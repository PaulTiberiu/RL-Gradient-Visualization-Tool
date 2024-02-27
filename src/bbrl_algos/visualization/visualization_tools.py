import numpy as np
import os
import torch


"""
def calculate_euclidean_distance(policy1, policy2):
    distance = 0.0
    for i in range (len(policy1)):
        distance += torch.norm(policy1[i] - policy2[i], p=2) #on fait torch.norm ou vraiment (policy1[i] - policy2[i])**2

    return distance
"""

def calculate_euclidean_distance(policy1, policy2):
    distance = torch.norm(policy1 - policy2, p=2)
    return distance.item()  # Convert to Python float


def calculate_gradient_normv2(model):
    total_norm = 0.0
    for param in model.parameters():
        if param.grad is not None:
            param_norm = torch.norm(param.grad.data, p=2)
            total_norm += param_norm.item()

    # or grad_norm = np.sqrt(sum([torch.norm(p.grad)**2 for p in model.parameters()]))

    return total_norm


def calculate_gradient_norm(model):
    total_norm = 0.0
    for param in model.parameters():
        if param.grad is not None:
            param_norm = torch.norm(param.grad.data, p=2)
            total_norm += param_norm.item() ** 2 # Add the squared norm
    total_norm = total_norm ** 0.5 # Take the square root of the sum of squared norms

    # or grad_norm = np.sqrt(sum([torch.norm(p.grad)**2 for p in model.parameters()]))

    return total_norm
   

def is_grad_norm_proportional_to_distance(cfg):
    
    eps = 0.02
    script_directory = os.path.dirname(os.path.abspath(__file__))

    distance_file_path = os.path.join(script_directory, "distances.txt")

    with open(distance_file_path, "r") as distance_file:
        distance_data = [float(line.strip()) for line in distance_file.readlines()]
    
    distance_values = [float(value) for value in distance_data]

    grad_file_path = os.path.join(script_directory, "gradient_norm.txt")

    with open(grad_file_path, "r") as grad_file:
        grad_data = [float(line.strip()) for line in grad_file.readlines()]
    
    grad_values = [float(value) for value in grad_data]

    for i in range(len(distance_values)):
        k = distance_values[i] / grad_values[i]
        #write_in_file("facteurs_k.txt", k) A FAIRE A LA MAIN
        #write_in_file("differences_grad_distances.txt", abs(k - cfg.optimizer.lr)) A FAIRE A LA MAIN CAR JE VEUX SUPPRIMER LE CONTENU DU FICHIER A CHAQUE FOIS


        if(abs(k - cfg.optimizer.lr) > eps):
            return False
            #print(abs(k - cfg.optimizer.lr))

    return True
