import pandas as pd

# reading off the text from the printing programme into an array
full_text = pd.DataFrame(
    [line.strip().split(" ")
     for line in open("example_unedited.txt", encoding="utf8")]
)

############################################################

# Write a function that removes  a row of a dataframe with
# a specific starting symbol in one of its elements or keeps
# all rows starting with a certain symbol


def kick_keep(text, symbols, keep):
    """Kicking or keeping rows with elements with certain symbols"""
    remaining = ~(text == True)  # Creating a dataframe of True
    remaining = remaining.any(axis=1)  # Creating a Series of True
    for i in symbols:
        # indices and columns that have the symbol
        indices = text.stack().str.contains(
            i,
            case=True,
        )
        # Checking which of the rows should be considered
        indices = indices.unstack().any(axis=1)
        if keep == True:
            remaining = remaining & indices
        elif keep == False:
            indices = ~indices
            remaining = remaining & indices
    text = text.loc[remaining]
    return text


############################################################

# Write a function that replaced wanted string elements with
# other string elements


def lets_replace(text, symbols, repl_symbols):
    for a, b in zip(symbols, repl_symbols):
        text = text.stack().str.replace(a, b).unstack()
    return text


############################################################

# Write a function that determines the "high" and "low" positions
# of the nozzle; "high" being when it is not touching the substrate,
# and "low" when it is. Luckily, when Flatcam generates a Gcode text
# file, it assumes that when the printing head is moving to a "low"
# position, it will have to mill the material. Therefore, G01 code is
# used in that case and that is the easiest way of determining, which
# position is "high" and which one is "low".


def high_low(text):
    z_indices = text[1].str.contains(
        "Z",
        case=True,
    )
    text_z = text.loc[z_indices, :]
    g00_indices = text_z[0].str.contains(
        "G00",
        case=True,
    )
    g00_indices = g00_indices[g00_indices].index
    g01_indices = text_z[0].str.contains(
        "G01",
        case=True,
    )
    g01_indices = g01_indices[g01_indices].index
    high_z = text_z.loc[g00_indices[0], 1]
    low_z = text_z.loc[g01_indices[0], 1]
    high_low_ans = [high_z, low_z]
    return high_low_ans


############################################################

# Need to keep everything that has G0 start:
full_text = kick_keep(full_text, ["G0"], keep=True)

# Need to remove the lines with max Z value (Z15) and all of the F codes
full_text = kick_keep(full_text, ["Z15", "F"], keep=False)

# # Need to find the "high" and "low" positions of the nozzle
high_low_list = high_low(full_text)
top_z = high_low_list[0]
bottom_z = high_low_list[1]

# Finding out the parameters that will be needed for converting the code
system = input(
    "Is the code written in Imperial or Metric (default) units? Write 'imperial' or 'metric' without apostrophes and press Enter: "
)
speed = input(
    "At what speed should the nozzle be moving, i.e. what is the feed rate? Please write a number and press Enter: "
)
top_position = input(
    "Z-coordinate for printing (the highest point of the stage)? Please write a number or type 'd' without apostrophes for the default value and press Enter: "
)
bottom_position = input(
    "Z-coordinate for moving the stage without printing (the lowest point of the stage)? Please write a number or type 'd' without apostrophes for the default value and press Enter: "
)
f_code = "F" + speed

# Writing the cases for the preamble if the system is metric or imperial
if system == "metric" or "Metric" or "m":
    preamble_list = [
        ["G90", None, None],
        ["G71", None, None],
        ["G94", None, None],
        ["G01", f_code, None],
        ["G00", "Z0.0000", None],
    ]
    preamble = pd.DataFrame(preamble_list)
    if top_position == "d":
        top_position = "17.5000"
    if bottom_position == "d":
        bottom_position = "16.5000"

elif system == "imperial" or "Imperial" or "i":
    preamble_list = [
        ["G90", None, None],
        ["G70", None, None],
        ["G94", None, None],
        ["G01", f_code, None],
        ["G00", "Z0.0000", None],
    ]
    preamble = pd.DataFrame(preamble_list)
    if top_position == "d":
        top_position = "0.68898"
    if bottom_position == "d":
        bottom_position = "0.64898"
else:
    preamble_list = [
        ["G90", None, None],
        ["G71", None, None],
        ["G94", None, None],
        ["G01", f_code, None],
        ["G00", "Z0.0000", None],
    ]
    preamble = pd.DataFrame(preamble_list)
    if top_position == "d":
        top_position = "17.5000"
    if bottom_position == "d":
        bottom_position = "16.5000"

# Making the correct string for positions
top_position = "Z" + top_position
bottom_position = "Z" + bottom_position

# Need to replace all "high" and "low" Z values with newer ones
# In this case, the top position refers to the bottom z because
# we are moving the stage rather than the nozzle (or the milling head)
full_text = lets_replace(full_text, [top_z, bottom_z], [
                         bottom_position, top_position])

# Create an ending
ending_list = [["G00", "Z0.0000", None], ["G00", "X0.0000", "Y0.0000"]]
ending = pd.DataFrame(ending_list)

# Concatenate all of the dataframes
printing_programme = pd.concat(
    [preamble, full_text, ending], ignore_index=True, axis=0)

# Write the dataframe to a text file
printing_programme.to_csv(
    "converted.txt",
    header=None,
    index=None,
    sep=" ",
    mode="a",
)
