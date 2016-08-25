# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""
Heavy lifting geometry for IDF surfaces.

PyClipper is used for clipping.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from geomeppy.vectors import Vector3D
from tests.pytest_helpers import almostequal


class Segment(object):
    """Line segment in 3D."""
    
    def __init__(self, *vertices):
        self.vertices = vertices
        self.p1 = vertices[0]
        self.p2 = vertices[1]
    
    @property
    def direction(self):
        return self.p2 - self.p2
    
    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r})'.format(class_name, self.vertices)
    
    def __neg__(self):
        return Segment(self.p2, self.p1)
    
    def __iter__(self):
        return (i for i in self.vertices)
    
    def is_collinear(self, other):
        if almostequal(other, self) or almostequal(other, -self):
            return True
        a = self.p1 - other.p1
        b = self.p1 - other.p2
        angle_between = a.cross(b)
        if almostequal(angle_between, Vector3D(0,0,0)):
            return True
        a = self.p2 - other.p1
        b = self.p2 - other.p2
        angle_between = a.cross(b)
        if almostequal(angle_between, Vector3D(0,0,0)):
            return True
        return False
            
    def on_poly_edge(self, poly):
        """Test if segment lies on any edge of a polygon
        
        Parameters
        ----------
        poly : Polygon3D
            The polygon to test against.
        
        Returns
        -------
        bool
        
        """
        for edge in poly.edges:
            if self.is_collinear(edge):
                return True
        return False

def test_collinear():
    # same line
    edge1 = Segment(Vector3D(0,0,0), Vector3D(1,1,1))
    edge2 = Segment(Vector3D(0,0,0), Vector3D(1,1,1))
    assert edge1.is_collinear(edge2)

    # opposite line
    edge1 = Segment(Vector3D(1,1,1), Vector3D(0,0,0))
    edge2 = Segment(Vector3D(0,0,0), Vector3D(1,1,1))
    assert edge1.is_collinear(edge2)

    # edge1 is longer
    edge1 = Segment(Vector3D(0,0,0), Vector3D(4,4,4))
    edge2 = Segment(Vector3D(1,1,1), Vector3D(2,2,2))
    assert edge1.is_collinear(edge2)

    # same start point, different lengths
    edge1 = Segment(Vector3D(0,0,0), Vector3D(1,1,1))
    edge2 = Segment(Vector3D(0,0,0), Vector3D(2,2,2))
    assert edge1.is_collinear(edge2)
    
    # something being missed
    edge1 = Segment(Vector3D(1,4,0), Vector3D(1,0,0))
    edge2 = Segment(Vector3D(1,0,0), Vector3D(1,2,0))
    assert edge1.is_collinear(edge2)
    
    # parallel
    edge1 = Segment(Vector3D(0,0,0), Vector3D(1,1,1))
    edge2 = Segment(Vector3D(1,0,0), Vector3D(2,1,1))
    assert not edge1.is_collinear(edge2)

    
    
    
    

