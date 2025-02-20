# XSection tests

# system modules
import math, os.path
import sys
import pytest
from math import pi

# my modules
from cadquery import *
from cqkit import *


triangle_pts = [(0, 0), (1, 0), (0, 3)]

round_pts = [
    (0, 0),
    (3, 0),
    (2.5, 0.5),
    (2.5, 4),
    {"radiusArc": ((2, 4.5), -0.5)},
    (0, 4.5),
]


def test_xsection_init():
    xc = XSection()
    pts = xc.get_points()
    assert len(pts) == 0

    xc = XSection(triangle_pts, "XZ", symmetric=False)
    pts = xc.get_points()
    assert len(pts) == 3

    xc = XSection(triangle_pts, "XZ", symmetric=True, mirror_axis="Z")
    pts = xc.get_points()
    assert len(pts) == 4


def test_xsection_geometry():

    xc = XSection(triangle_pts, "XZ", symmetric=False)
    pts = xc.get_points()
    assert (0, 3) in pts
    assert (-1, 0) not in pts

    xc = XSection(triangle_pts, "XZ", symmetric=True, mirror_axis="Z")
    pts = xc.get_points()
    assert (0, 3) in pts
    assert (-1, 0) in pts

    pts = xc.get_points(flipped=True)
    assert (0, -3) in pts
    assert (0, 3) not in pts
    assert (-1, 0) in pts

    pts = xc.get_points(scaled=2)
    assert (2, 0) in pts
    assert (0, 6) in pts
    assert (-2, 0) in pts

    pts = xc.get_points(scaled=(0.5, 3))
    assert (0.5, 0) in pts
    assert (0, 9) in pts
    assert (-0.5, 0) in pts

    pts = xc.get_points(translated=(-2, 4))
    assert (-2, 4) in pts
    assert (-1, 4) in pts
    assert (-2, 7) in pts
    assert (-3, 4) in pts

    triangle2_pts = [(0, 0), (0, 3), (1, 0)]
    xc = XSection(triangle2_pts, "XZ", symmetric=True, mirror_axis="X")
    pts = xc.get_points()
    assert (0, -3) in pts
    assert (1, 0) in pts
    assert (-1, 0) not in pts


def test_xsection_outline():

    xc = XSection(triangle_pts, "XZ", symmetric=True, mirror_axis="Z")
    pts = xc.get_points()

    r = xc.render()
    wires = r.wires().vals()
    assert len(wires) == 1
    edges = r.edges().vals()
    assert len(edges) == 4

    r = xc.get_bounding_outline()
    edges = r.edges().vals()
    assert len(edges) == 4
    pts = r.vertices().vals()
    tpts = vertices_to_tuples(pts)
    assert (-1, 0, 0) in tpts
    assert (-1, 0, 3) in tpts
    assert (1, 0, 3) in tpts
    assert (1, 0, 0) in tpts

    r = xc.get_bounding_rect()
    assert r.left == -1
    assert r.right == 1
    assert r.top == 3
    assert r.bottom == 0
    assert r.width == 2
    assert r.height == 3


def test_xsection_solid():

    xc = XSection(triangle_pts, "XZ", symmetric=True, mirror_axis="Z")
    r = xc.render().extrude(7)

    faces = r.faces().vals()
    assert len(faces) == 5
    wires = r.wires().vals()
    assert len(wires) == 5
    vtx = r.vertices().vals()
    tpts = vertices_to_tuples(vtx)

    assert (1, -7, 0) in tpts
    assert (-1, 0, 0) in tpts
    assert (-1, -7, 0) in tpts
    assert (0, -7, 3) in tpts

    xc = XSection(triangle_pts, "XZ", symmetric=True, mirror_axis="Z")
    r = xc.render().extrude(-7)

    faces = r.faces().vals()
    assert len(faces) == 5
    wires = r.wires().vals()
    assert len(wires) == 5
    vtx = r.vertices().vals()
    tpts = vertices_to_tuples(vtx)

    assert (1, 7, 0) in tpts
    assert (-1, 0, 0) in tpts
    assert (-1, 7, 0) in tpts
    assert (0, 7, 3) in tpts
