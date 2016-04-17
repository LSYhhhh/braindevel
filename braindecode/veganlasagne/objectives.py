import lasagne
from braindecode.veganlasagne.layers import get_n_sample_preds
from lasagne.objectives import categorical_crossentropy
from theano.tensor.shared_randomstreams import RandomStreams
from lasagne.random import get_rng
import theano.tensor as T

def weighted_binary_cross_entropy(preds, targets, imbalance_factor):
    factor_no_target = (imbalance_factor + 1) / (2.0 *  imbalance_factor)
    factor_target = (imbalance_factor + 1) / 2.0
    loss = lasagne.objectives.binary_crossentropy(preds, targets)
    loss = factor_no_target * loss + loss * targets * factor_target
    return loss

def sum_of_losses(preds, targets, final_layer, loss_expressions):
    all_losses = []
    for expression in loss_expressions:
        try:
            loss = expression(preds, targets)
        except TypeError:
            loss = expression(preds, targets, final_layer)
        if loss.ndim > 1:
            loss = loss.mean()
        all_losses.append(loss)
        
    total_loss = sum(all_losses)
    return total_loss

def weight_decay(preds, targets, final_layer, factor):
    loss = lasagne.regularization.regularize_network_params(final_layer,
        lasagne.regularization.l2)
    return loss * factor

def tied_losses_cnt_model(preds, targets, final_layer, n_pairs):
    n_sample_preds = get_n_sample_preds(final_layer)
    n_classes = final_layer.output_shape[1]
    return tied_losses(preds, n_sample_preds, n_classes, n_pairs)

def tied_losses(preds, n_sample_preds, n_classes, n_pairs):
    preds_per_trial_row = preds.reshape((-1, n_sample_preds, n_classes))
    _srng = RandomStreams(get_rng().randint(1, 2147462579))
    rand_inds = _srng.choice([n_pairs  * 2], n_sample_preds, replace=False)
    part_1 = preds_per_trial_row[:,rand_inds[:n_pairs]]
    part_2 = preds_per_trial_row[:,rand_inds[n_pairs:]]
    # Have to now ensure first values are larger zero
    # for numerical stability :/
    eps = 1e-4
    part_1 = T.maximum(part_1, eps)
    loss = categorical_crossentropy(part_1, part_2)
    return loss

def tied_neighbours_cnt_model(preds, targets, final_layer):
    n_sample_preds = get_n_sample_preds(final_layer)
    n_classes = final_layer.output_shape[1]
    return tied_neighbours(preds, n_sample_preds, n_classes)

def tied_neighbours(preds, n_sample_preds, n_classes):
    preds_per_trial_row = preds.reshape((-1, n_sample_preds, n_classes))
    earlier_neighbours = preds_per_trial_row[:,:-1]
    later_neighbours = preds_per_trial_row[:,1:]
    # Have to now ensure first values are larger zero
    # for numerical stability :/
    # Example of problem otherwise:
    """
    a = T.fmatrix()
    b = T.fmatrix()
    soft_out_a =softmax(a)
    soft_out_b =softmax(b)
    
    loss = categorical_crossentropy(soft_out_a[:,1:],soft_out_b[:,:-1])
    neigh_fn = theano.function([a,b], loss)
    
    neigh_fn(np.array([[0,1000,0]], dtype=np.float32), 
        np.array([[0.1,0.9,0.3]], dtype=np.float32))
    -> inf
    """
    eps = 1e-4
    earlier_neighbours = T.maximum(earlier_neighbours, eps)
    # not sure if necessary
    earlier_neighbours = T.minimum(earlier_neighbours, 1-eps)
    # renormalize(?)
    earlier_neighbours = earlier_neighbours / T.sum(earlier_neighbours, axis=2, keepdims=True)
    loss = categorical_crossentropy(earlier_neighbours, later_neighbours)
    return loss
    