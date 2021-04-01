import  argparse

args = argparse.ArgumentParser()
# args.add_argument('--train_data_dir', default='./matrix_data_sroie/')
args.add_argument('--train_data_dir', default='./graph/data/train_matrixs/')
args.add_argument('--test_data_dir', default='./graph/data/test_matrixs/')
args.add_argument('--test_csv', default='./graph/data/test_csv/')
args.add_argument('--test_images', default='./graph/data/test_images/')
args.add_argument('--model', default='gcn')
args.add_argument('--learning_rate', type=float, default=0.001)
args.add_argument('--epochs', type=int, default=500)
args.add_argument('--hidden', type=int, default=128)
args.add_argument('--hidden1', type=int, default=64)
args.add_argument('--dropout', type=float, default=0.1)
args.add_argument('--weight_decay', type=float, default=5e-4)
args.add_argument('--early_stopping', type=int, default=10)
args.add_argument('--max_degree', type=int, default=3)


args = args.parse_args()
print(args)