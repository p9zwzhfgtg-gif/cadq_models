from cadquery import *

# Common Plate
cp_length = 31
cp_width = 23
cp_height = 1.5


# sim card
sc_length = 12.5
sc_width = 9
sc_height = 0.8

wall = 1

# sim card ejector (sc_ejector)
sce_length = 29.7
sce_width = 7.6
sce_height = 0.8


plate = (
    Workplane("XY")
    .box(cp_length, cp_width, cp_height)
    .faces(">Z")
    .workplane()
    .pushPoints([(-7, 0), (7, 0)])
    .hole(5, 1)
)

cover = (
    Workplane("XY")
    .box(cp_length, cp_width + 2.1, 1)
    .translate((0, 0, 1.3))
    .faces("<Z")
    .workplane()
    #     .center(0, 11.8)
    #     .rect(3, 0.5)f
    #     .extrude(1.5)
)
cover = cover.center(0, 12.05).rect(cp_length, 1).extrude(1.6)
cover = cover.center(0, -(12.05 * 2)).rect(cp_length, 1).extrude(1.6)

c_groove_l = (
    Workplane("ZY")
    .polygon(3, 1.7)
    .extrude(cp_length)
    .rotateAboutCenter((1, 0, 0), 31)
    .translate((cp_length / 2, -(12 - 0.7), 0))
)
c_groove_r = (
    Workplane("ZY")
    .polygon(3, 1.7)
    .extrude(cp_length)
    .rotateAboutCenter((1, 0, 0), -31)
    .translate((cp_length / 2, (12 - 0.7), 0))
)
cover = cover + c_groove_l
cover = cover + c_groove_r


groove_r = (
    Workplane("ZY")
    .polygon(3, 1.7)
    .extrude(40)
    .rotateAboutCenter((1, 0, 0), 31)
    .translate((20, -(12 - 0.9), 0))
)

groove_l = (
    Workplane("ZY")
    .polygon(3, 1.7)
    .extrude(40)
    .rotateAboutCenter((1, 0, 0), -31)
    .translate((20, (12 - 0.9), 0))
)


sim_card_dummy = (
    plate.faces(">Z")
    .workplane(offset=-1.0)
    .rect(sc_length, sc_width)
    .extrude(1, combine=False)
)


sc_ejector = (
    plate.faces(">Z")
    .workplane(offset=-1.0)
    .rect(sce_length, sce_width)
    .extrude(1, combine=False)
)


plate = plate - sim_card_dummy.translate((7, 5, 0))
plate = plate - sim_card_dummy.translate((-7, 5, 0))
plate = plate - sc_ejector.translate((0, -5, 0))
plate = plate - groove_r
plate = plate - groove_l


show_object(cover)
show_object(plate)

# Export
exporters.export(plate, "./export/simcard_plate.stl")
exporters.export(cover, "./export/simcard_cover.stl")
