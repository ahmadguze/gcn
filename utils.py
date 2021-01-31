import  torch
from    torch import nn
from    torch.nn import functional as F

def masked_loss(preds, labels, mask):
    """Softmax cross-entropy loss with masking."""
    loss = F.cross_entropy(preds, labels, reduction='none')
    mask = mask.float()
    mask = mask / mask.mean()
    loss *= mask
    loss = loss.mean()
    return loss

# add by hengli
def weighted_loss(preds, labels, weights):
    """Softmax cross-entropy loss with weights."""
    # criteron = nn.CrossEntropyLoss()
    # loss = criteron(preds, labels)

    loss = F.cross_entropy(preds, labels, reduction='none')
    weights = weights.float()
    loss *= weights
    loss = loss.mean()
    return loss

def masked_acc(out, label, mask):
    # [node, f]
    pred = out.argmax(dim=1)
    correct = torch.eq(pred, label).float()
    mask = mask.float()
    mask = mask / mask.mean()
    correct *= mask
    acc = correct.mean()
    return acc

# add by hengli
def cal_accuracy(out, label):
    "Accuracy in single graph."

    pred = out.argmax(dim=1)
    correct = torch.eq(pred, label).float()
    acc = correct.mean()
    return acc


def sparse_dropout(x, rate, noise_shape):
    """

    :param x:
    :param rate:
    :param noise_shape: int scalar
    :return:
    """
    random_tensor = 1 - rate
    random_tensor += torch.rand(noise_shape).to(x.device)
    dropout_mask = torch.floor(random_tensor).byte()
    i = x._indices() # [2, 49216]
    v = x._values() # [49216]

    # [2, 4926] => [49216, 2] => [remained node, 2] => [2, remained node]
    i = i[:, dropout_mask]
    v = v[dropout_mask]

    out = torch.sparse.FloatTensor(i, v, x.shape).to(x.device)

    out = out * (1./ (1-rate))

    return out


def dot(x, y, sparse=False):
    if sparse:
        res = torch.sparse.mm(x, y)
    else:
        res = torch.mm(x, y)

    return res

