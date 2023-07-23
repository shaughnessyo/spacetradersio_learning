from pytermgui import Container, Label, Splitter, Button, Checkbox

container = Container(
    Label("[bold accent]This is my example"),
    Label(""),
    Label("[surface+1 dim italic]It is very cool, you see"),
    Label(""),
    Splitter(
        Label("My first label", parent_align=0),
        Button("Some button", parent_align=2),
    ),
    Splitter(
        Label("My second label"),
        Checkbox(),
    ),
    Label(""),
    Splitter(Label("Left side"), Label("Middle"), Label("Right side")),
    Label(""),
    Button("Submit button")
)



