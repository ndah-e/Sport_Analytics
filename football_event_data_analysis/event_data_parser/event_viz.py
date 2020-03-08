import logging
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import seaborn as sns


# Draw field
class EventViz:
    """Class to visualize events"""
    def __init__(self, n_level=10):
        self.n_level = n_level

    def draw_field(self):
        """Draw a football field"""
        fig = plt.figure()
        fig.set_size_inches(7, 5)
        ax = fig.add_subplot(1, 1, 1)

        # Pitch Outline & Centre Line
        plt.plot([0, 0], [0, 90], color="black")
        plt.plot([0, 130], [90, 90], color="black")
        plt.plot([130, 130], [90, 0], color="black")
        plt.plot([130, 0], [0, 0], color="black")
        plt.plot([65, 65], [0, 90], color="black")

        # Left Penalty Area
        plt.plot([16.5, 16.5], [65, 25], color="black")
        plt.plot([0, 16.5], [65, 65], color="black")
        plt.plot([16.5, 0], [25, 25], color="black")

        # Right Penalty Area
        plt.plot([130, 113.5], [65, 65], color="black")
        plt.plot([113.5, 113.5], [65, 25], color="black")
        plt.plot([113.5, 130], [25, 25], color="black")

        # Left 6-yard Box
        plt.plot([0, 5.5], [54, 54], color="black")
        plt.plot([5.5, 5.5], [54, 36], color="black")
        plt.plot([5.5, 0.5], [36, 36], color="black")

        # Right 6-yard Box
        plt.plot([130, 124.5], [54, 54], color="black")
        plt.plot([124.5, 124.5], [54, 36], color="black")
        plt.plot([124.5, 130], [36, 36], color="black")

        # Prepare Circles
        centre_circle = plt.Circle((65, 45), 9.15, color="black", fill=False)
        centre_spot = plt.Circle((65, 45), 0.8, color="black")
        left_pen_spot = plt.Circle((11, 45), 0.8, color="black")
        right_pen_spot = plt.Circle((119, 45), 0.8, color="black")

        # Draw Circles
        ax.add_patch(centre_circle)
        ax.add_patch(centre_spot)
        ax.add_patch(left_pen_spot)
        ax.add_patch(right_pen_spot)

        # Prepare Arcs
        left_arc = Arc((11, 45), height=18.3, width=18.3, angle=0, theta1=310, theta2=50, color="black")
        right_arc = Arc((119, 45), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color="black")

        # Draw Arcs
        ax.add_patch(left_arc)
        ax.add_patch(right_arc)

        # Tidy Axes
        plt.axis('off')

    def heatmap(self, x, y):
        """Draw events as heatmap.
            :param x: x-coordinate where event ends
            :param y: y-coordinate of events origin
        """
        self.draw_field()
        sns.kdeplot(x, y, shade=True, n_levels=self.n_level)
        plt.ylim(0, 90)
        plt.xlim(0, 150)

        # Display Pitch
        plt.show()

    def draw_passes_old(self, x_origin, y_origin, x_end, y_end):
        """Draw passes.
            :param y_end: y-coordinate where event ends
            :param y_origin: y_coordinate of events origin
            :param x_end: x-coordinate where event ends
            :param x_origin: x-coordinate of the event origin
        """
        self.draw_field()
        for i in range(len(x_origin)):
            plt.plot([int(x_origin[i]), int(x_end[i])], [int(y_origin[i]), int(y_end[i])], color="blue")
            plt.plot(int(x_origin[i]), int(y_origin[i]), "o", color="green")

        # Display Pitch
        plt.show()

    def draw_passes(self, x_origin, y_origin, x_end, y_end):
        """ Draw passes
            :param y_end: y-coordinate where event ends
            :param y_origin: y_coordinate of events origin
            :param x_end: x-coordinate where event ends
            :param x_origin: x-coordinate of the event origin
        """

        self.draw_field()
        for i in range(len(x_origin)):
            plt.plot([int(x_origin[i]), int(x_end[i])], [int(y_origin[i]), int(y_end[i])],
                     color="blue")
            plt.plot(int(x_origin[i]), int(y_origin[i]), "o", color="green")
        # Display Pitch
        plt.show()
