import matplotlib.pyplot as plt


def show_colors_with_hex_codes(color_list):
    fig, ax = plt.subplots(facecolor="#2B2B2B")

    # Set up the plot parameters
    ax.set_xlim([0, 10])
    ax.set_ylim([0, len(color_list)])
    ax.set_axis_off()

    for i, color in enumerate(color_list):
        # Draw a rectangle with the color
        ax.add_patch(plt.Rectangle((1, i), 8, 1, color=color_list[color]))

        # Add the color hex code as text
        ax.text(
            9, i + 0.5, f"{color}: {color_list[color]}", va="center", color="#AEB5BD"
        )

    plt.show()
    # plt.savefig("color_plot.png")


# Example list of hex color codes
colors = {
    "#text": "#AEB5BD",  # text
    "#keywords": "#597CC2",  # keywords
    "#jsonkey": "#828EBA",  # jsonkey
    "#packages": "#7393BF",  # packages
    "#variables": "#4EADE5",  # variables
    "#function": "#D9AF6C",  # function
    "#local_function": "#BF9E5C",  # local function
    "#string": "#807D6E",  # string
}
# colors = [
#     # "#AEB5BD",  # text
#     # "#597CC2",  # keywords
#     # "#828EBA",  # jsonkey
#     # "#7393BF",  # pakages
#     # "#4EADE5",  # variables
#     # "#D9AF6C",  # function
#     # "#BF9E5C",  # local function
#     # "#807D6E",  # string
#     # "#7A7A7A",
#     # "#828EBA",  # - json key
#     # "#267DFF",
#     # "#E57132",
#     # "#E8BF6A",  # css
#     # "#66A6FF",
#     # "#0F9795",
#     # "#93A629",
#     # "#4646F1",
#     # "#BD693C",
#     # "#99956B",
#     # "#ABC023",
#     # "#5394EC",
#     # "#299999",
#     # select
#     # "#436571",
#     # "#714950",
#     # "#50416E",
#     # "#734C3A",
#     # "#A47A36",
#     # "#2F4794",
#     # "#589DF6",
#     # "#287BDE",
# ]


show_colors_with_hex_codes(colors)
