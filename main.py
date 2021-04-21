import pandas as pd
from Population import Population
import matplotlib.pyplot as plt
from utils import *


def plot_score_in_time(history):
    fig = plt.figure(dpi=150)

    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(history['Training Loss'], '-b', label='Training Loss')
    ax1.plot(history['Validation Loss'], '-r', label='Validation Loss')
    ax1.legend(loc='upper right', frameon=False)
    ax1.set_ylabel('Loss value')
    ax1.set_xlabel('Epoch')
    ax1.set_title('Loss during training')

    ax1 = fig.add_subplot(1, 2, 2)
    ax1.plot(history['Training Accuracy'], '-b', label='Training Accuracy')
    ax1.plot(history['Validation Accuracy'], '-r', label='Validation Accuracy')
    ax1.legend(loc='lower right', frameon=False)
    ax1.set_ylabel('Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_title('Accuracy during training')

    fig.tight_layout()

    plt.show()


def training(continue_training=False):
    nn = None
    try:
        df = pd.read_csv(DATASET_FILE_NAME)
        x = files_to_img_list(df['file'].tolist())
        y = df['label'].tolist()
    except FileNotFoundError as ex:
        print("Warning! No such directory was found.")
        return
    if continue_training:
        try:
            nn = load_nn()
        except Exception as ex:
            print("Cannot load nn, start training from scratch.")
            training()
        training_history = pd.read_csv(TRAINING_HISTORY_FILE_NAME)
        pop = Population(POPULATION_SIZE, x, y, SIMULATION_LENGTH, OUTPUT_LABELS, best_nn=nn)
    else:
        training_history = pd.DataFrame(columns=TRAINING_HISTORY_COLUMNS)
        pop = Population(POPULATION_SIZE, x, y, SIMULATION_LENGTH, OUTPUT_LABELS)
    for i in range(NUM_OF_EPOCH):
        pop.create_new_population()
        pop.session_for_dinos()
        t_loss = pop.get_min_loss()
        t_acc = pop.get_max_score()
        v_acc, v_loss = pop.validate()
        print("\n\n-------------- EPOCH N-{0} --------------".format(i + 1))
        print("Training accuracy: {:.2f}".format(t_acc))
        print("Training loss: {:.2f}".format(t_loss))
        print("Validation accuracy: {:.2f}".format(v_acc))
        print("Validation loss: {:.2f}".format(v_loss))
        training_history = training_history.append({col: value for col, value in
                                                    zip(TRAINING_HISTORY_COLUMNS, [t_loss, t_acc, v_loss, v_acc])},
                                                   ignore_index=True)
        training_history.to_csv(TRAINING_HISTORY_FILE_NAME, index=False)
        save_nn_to_file(pop.get_best_nn())

    plot_score_in_time(training_history)


def validate():
    v_score = 0
    try:
        df = pd.read_csv(DATASET_FILE_NAME)
        x = files_to_img_list(df['file'].tolist())
        y = df['label'].tolist()
        _, validation = get_train_and_valid(x, y)
    except FileNotFoundError as ex:
        print("Warning! No such directory was found.")
        return

    try:
        nn = load_nn()
    except Exception as ex:
        print(ex)
        print("Cannot load nn")
        return
    for i in validation:
        img, label = i
        if OUTPUT_LABELS[nn.predict(img).argmax()] == label:
            v_score += 1
            print(nn.predict(img), label)
    print(v_score / len(validation))

if __name__ == '__main__':
    choice = input("Choose mode t - Start training, v - Validate existing nn, "
                   "c - Continue training, p - Plot training history: ")
    if choice == 't':
        training()
    elif choice == 'v':
        validate()
    elif choice == 'c':
        training(continue_training=True)
    elif choice == 'p':
        plot_score_in_time(pd.read_csv(TRAINING_HISTORY_FILE_NAME))
