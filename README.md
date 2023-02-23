# General Info
With UDEfix the user can model systems or rather their underlying fixpoint equations and verify whether some fixpoint is the least or greatest fixpoint.
It may also detect that some post/pre-fixpoint is a lower/upper bound for the least/greatest fixpoint. A key feature of UDEfix is that these usually
complicated fixpoint functions can be disassembled into smaller subfunctions. Here, we use composition and disjoint unsion to assemble larger functions.
This allows the user to assemble his very own fixpoint equation from the given smaller subfunctions.



# How to use UDEfix
Open up <main.exe> in the main directory to start the tool. The tool is divided into three main areas: the "Content"- (left side), the "Basic functions"-
(right side) and the "Building"-Area (middle). Additionally you can chose the MV-algebra that will be used for all calculations under File->Settings. To
find out the definition of the different MV-Algebras, you can hover over them


## "Content"-Area
In the "Content"-Area you can create different mappings, relations and sets that can be used in the functions of the "Building"-Area. New elements can
be added by entering a name and pressing the "+"-button below the list of mappings/relations/sets. This will open up a new window, where different
adjusments can be made, depending on the type of content. The content can be saved under File->Save Content and other content files can be opened
accordingly.

### Mappings
The mapping type decides where the mapping can be used. This could be anywhere, in the corresponding function nodes (see "Basic Functions"-Area) or only
when creating sets of mappings or other mappings. You can find the detailed list with "Type" and "Usage" below:

constant	-> constant function-node + creating sets
reindexing	-> reindexing function-node + creating sets
arithmetic	-> addition, subtraction and subtraction^z function-nodes + creating sets
testing		-> testing function-node + creating sets
miscellaneous	-> creating sets or other mappings
all		-> anywhere

The mapping also has a domain and a codomain. As domains you can either choose an already created set, the current MV-algebra or "custom set" to create
a mapping without having to create a new set. If "custom set" is chosen, the type of the set has to be declared and if "MV-algebra" is chosen, the used
MV-algebra can be changed. By pressing the "+"-button in the bottom right, new mappings can be defined. If the domain is a custom set, there is also the
possibility to press the "++"-button, which will automatically create default definitions for every element in the set.

### Relations
There are currently three different relation types that can be used. For any type you have to choose two sets to create a relation from the first set to
the second set. If the "custom"-type is used, you can create your own relation by checking the checkboxes in the content below. For the other two types
the content is not visible until the "Show content"-button is pressed. This is because the relations will be calculated automatically and the checkboxes
dont have to be checked manually. Also these relations tend to be a little bigger and this might cause lag. I would recommend to only press the button
if the sets are not that big or you want to take a look at how the relation looks like.

The "is-element-of"-relation sets all the elements x of the first set in relation with the elements y of the second relation, if x is an element of y.

For the "projection"-relation you additionally have to chose a projection type. If for example the projection type "(x, y) -> x" is used, all the
elements (a, b) will be set in relation with all the elements c of the second relation, if a = c. Obviously, the first set has to be a set of tuples
in this case. The same restrictions apply for all the other projection types.

### Sets
To create a set you only have to chose the type of the set. Beside the usual types, you also have the option to create a set by using different set-
operators on other sets, for example the power set. Furthermore there is the possibility to create a set with n elements without having to name every
element.


## "Basic functions"-Area
In the "Basic funtions"-Area there is not much you can do on its own. It contains all the functions that can be used in the "Building"-Area. This can
be done by dragging the function into the area, if there is an open file. The "Basic functions"-Area is divided into two parts. The upper functions are
all functions from Table 2 (see Tool Paper). The two functions below that are a little bit different: The "Higher-Order Function" creates a node that
acts like a placeholder, in the "testing" function the final function will be displayed and can be tested (for more information: see "Building"-Area).


## "Building"-Area
The "Building"-Area can be opened by opening a (new) file (File->New / File->Open). Now you can create new nodes by dragging a function from the
"Basic functions"-Area and dropping it into the "Building"-Area or by pressing Right-Click and choosing one of the functions. Function-nodes have up
to 3 sockets.

### Upper functions
All upper functions of the "Basic functions"-Area have 2 sockets. From these sockets, edges can be drawn to sockets of other nodes. Connecting the 
right/output socket of a function with the left/input socket of another function, equals the composition of these two functions. The disjoint union is
achieved by connecting more than one function to the left/input socket of a function. The upper functions also have parameter-boxes. These boxes can be
filled in with sets, mappings and relations, which have been defined in the "Content"-Area. Every function has atleast two parameters, the input and
the output set. These sets are the corresponding domain and codomain of the the function. Additionally some functions need a third parameter, depending
on the used function (see Table 2 - Tool Paper).

Please note that the requirements for the composition and the disjoint union also holds for connecting nodes in the tool. This means that for example
the output set of the first node and the input set of the second node has to be same, if they are connected to each other. If this is not the case, a
red exclamation mark will be displayed on the top right of the node. You can hover over the mark to learn more about the error.

### Lower functions
The "Higher-Order Function" acts like as a placeholder that has a third socket and thus can be connected from below. The connected function will be
displayed in the node and can be integrated in an even bigger function exactly like all the upper functions.

The "Testing"-function-node is essential for testing the function and should be usually created once. It only has a left/input socket and thus acts
like the end of the function. After connecting the complete function without any errors (green mark on the top left), you can now test the displayed
function. After chosing a mapping, press the "Compute"-button to test if the mapping is a fixpoint, pre-fixpoint and/or post-fixpoint. If the mapping
is a fixpoint, you also get the chance to test if it is the greatest or/and the least fixpoint. If it only is a pre- or post-fixpoint, you can test
if the greatest fixpoint is smaller or equal to it or if the mapping is smaller or equal to the least fixpoint.

Additionally you can compute iota (see Tool paper), if the mapping is a fixpoint, but not the least and the greatest fixpoint. This part is still in work
and I am not sure if it actually shows the correct values. If you want more information about the calculations you can take a look at the console that
should start together with the program. For the first computation, for example, the console prints out the value of the mapping for each element in the
input set before and after the application of the function.


## Example content and graphs
For an easier start I recommend to take a look at the already created content and graphs of some examples in <fixpointtool/content> and
<fixpointtool/graphs>. These include the following examples: termination probability, stochastic games, energy games and bisimilarity. There is also
a content file <content_types> which includes sets, mappings and relations of all possible types in the tool. Furthermore, if you want to create the
content of one of the mentioned examples (except energy games (not implemented yet)), you can do this a little bit faster by importing it from an .xlsx
file under File->Import graph. This works only if the .xlsx file has a defined structure. You can find these by checking out the examples in
<fixpointtool/content/excel>.


## Additional Shortcuts/Features
There are some shortcuts and features that are not shown directly under the tabs "File", "Edit" and "Window". These are all for the "Building"-Area.
- You can draw a box around (multiple) functions and edges to move, copy, cut or delete them by pressing and holding the left mouse button
- You can press and hold the middle mouse button to move the area
- You can use the mouse wheel to zoom the area in and out
- You can use Ctrl+LMB (Hold) to delete multiple edges at once


## Additional Info
The tool has still many bugs and might crash here and there. That is why you should probably save your changes regularly.