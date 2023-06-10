import numpy as np
import logging

def generate_generation_data_set(data, num_sample, img_offset):
    orig_img_id = []
    print(data.data.size)
    imgs = data.data.detach().numpy()
    print(data.data.shape)
    labels = data.labels #
    imgs = imgs[img_offset:num_sample + img_offset]
    labels = np.argmax(labels[img_offset:num_sample + img_offset],1)
    for sample_index in range(imgs.shape[0]):
        orig_img_id.append(sample_index)
    return imgs, labels, labels, orig_img_id

def generate_attack_data_set(data, model):
    pred_labels = np.argmax(model(data.data.float()).detach().numpy(), 1)
    true_labels = np.argmax(data.labels ,1)

    correct_data_indices = np.where([1 if x == y else 0 for (x, y) in zip(pred_labels, true_labels)])

    logging.info("Total testing data:{}, correct classified data:{}".format(len(data.labels), len(correct_data_indices[0])))
    imgs = data.data[correct_data_indices].detach().numpy()
    labels = np.argmax(data.labels[correct_data_indices] ,1) #
    orig_img_id = np.array(correct_data_indices)
    return imgs, labels, labels, orig_img_id
