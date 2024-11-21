import numpy as np
import pandas as pd

# reading off the text from the printing programme into an array
full_text = pd.DataFrame([line.strip().split(" ")
                         for line in open("converted.txt")])
# parsing through the text to find the indices of rows and the corresponding z-coordinates
z_coordinates = full_text.stack()[
    full_text.stack().str.contains("z", case=False)
].unstack()
# print(z_coordinates)

# finding the first and last names of the rows with z-coordinates
all_row_name = z_coordinates.index.values.tolist()  # a list of values of every row
first_row_name = all_row_name[0]  # value of the row of the first z-coordinate
last_row_name = all_row_name[-1]  # value of the row of the last z-coordinate

# cutting out the whole beginning before the first z-coordinate
preamble = full_text.loc[0: first_row_name - 1]

# cutting out the ending of the code where we home the stage to (0,0,0)
ending = full_text.loc[last_row_name:]

# cutting out only the chunk of text that will be updated
single_layer = full_text.loc[first_row_name: last_row_name - 1]
# print(single_layer)

# adjusting z_coordinates to remove the Z0.0000 row because that row is not going to be iterated
z_coordinates = z_coordinates.drop(last_row_name)

# asking for a specific number of layers
no_layers = int(
    input("Enter the number of layers of ink that you wish to print: "))

# asking for the incremental shift in z-axis position with every layer
z_increment = np.float64(
    input("Enter the incremental shift in the z-axis position: "))

# creating a dataframe for the total printing programme
main_text = single_layer.stack().unstack()
# stack and unstack functions are used so that an actual copy is made, otherwise the copy is made only when main_text is
# called and that is after the adjustment to the coordinates

# striping the z coordinates of the 'Z'
z_coordinates = pd.DataFrame(z_coordinates.squeeze().str.replace("Z", ""))

# converting the z coordinates from strings to float numbers
z_coordinates = pd.DataFrame(pd.to_numeric(z_coordinates.squeeze()))

# need to know which elements in the array need to be replaced in the upcoming for loop
z_coordinates_rows = z_coordinates.index.values.tolist()

# just some code I am writing for the sake of testing out how concatenation works and finding out what is wrong with the
# the code I have written so far

# let's do the first shift in the z-coordinates
# new_block_z_1=pd.DataFrame(z_coordinates.squeeze()-z_increment)
# new_block_z_1=pd.DataFrame('Z' + new_block_z_1.squeeze().astype(str))
# single_layer.loc[z_coordinates_rows,1]=new_block_z_1.squeeze()
# print(single_layer)

# let's concatenate this first bit with the bit after the first shift
# main_text=pd.concat([main_text,single_layer],ignore_index=True,axis=0)
# print(main_text)

# creating a loop to update the z-coordinates for every layer and add the block for every layer to the total printing programme
for i in range(1, no_layers):
    new_block_z = pd.DataFrame(
        round((z_coordinates.squeeze() - z_increment * i), 5)
    )  # updating the z-coordinates
    new_block_z = pd.DataFrame(
        "Z" + new_block_z.squeeze().astype(str)
    )  # adding Z in the string
    single_layer.loc[
        z_coordinates_rows, 1
    ] = new_block_z.squeeze()  # replacing the Z-coordinates in the single layer block
    main_text = pd.concat(
        [main_text, single_layer], ignore_index=True, axis=0
    )  # stacking the new block under the code we have so far

# stacking all the needed building blocks to create the full text for the printing programme
printing_programme = pd.concat(
    [preamble, main_text, ending], ignore_index=True, axis=0)
print(printing_programme)
printing_programme.to_csv("3d_printing.txt", header=None,
                          index=None, sep=" ", mode="a")
