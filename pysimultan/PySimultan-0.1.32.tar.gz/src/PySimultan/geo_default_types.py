from weakref import WeakSet
import numpy as np
import colorlog
from .utils import classproperty, get_obj_by_id

from .config import cs_axis_up
from .ParameterStructure.Instances import InstanceType
# from copy import deepcopy
# from functools import lru_cache
from tqdm import tqdm
from copy import copy

logger = colorlog.getLogger('PySimultan')


# class classproperty(object):
#
#     def __init__(self, getter):
#         self.getter = getter
#
#     def __get__(self, instance, owner):
#         return self.getter(owner)
#
#
# class GeometryModel(object):
#
#     _cls_instances = WeakSet()      # weak set with all created objects
#     _create_all = False             # if true all properties are evaluated to create python objects when initialized
#
#     @classproperty
#     def _cls_instances_dict(cls):
#         return dict(zip([x.id for x in cls._cls_instances], [x() for x in cls._cls_instances]))
#
#     @classproperty
#     def cls_instances(cls):
#         return list(cls._cls_instances)
#
#     def __new__(cls, *args, **kwargs):
#         instance = super().__new__(cls)
#         if "_cls_instances" not in cls.__dict__:
#             cls._cls_instances = WeakSet()
#         try:
#             cls._cls_instances.add(instance)
#         except Exception as e:
#             logger.error(f'Error adding instance {instance} to _cls_instances: {e}')
#
#         return instance
#
#     def __init__(self, *args, **kwargs):
#         self._wrapped_obj = kwargs.get('wrapped_obj', None)
#
#         self._vertices = kwargs.get('vertices', None)
#         self._edges = kwargs.get('edges', None)
#         self._edge_loops = kwargs.get('edge_loops', None)
#         self._faces = kwargs.get('faces', None)
#         self._volumes = kwargs.get('volumes', None)
#         self._layers = kwargs.get('layers', None)
#
#         self.GeoBaseClass, self.LayerCls, self.VertexCls, self.EdgeCls, self.EdgeLoopCls, self.FaceCls, self.VolumeCls = create_geo_classes()
#         self.load_all()
#
#     @property
#     def id(self):
#         return self._wrapped_obj.Id
#
#     @property
#     def name(self):
#         if self._wrapped_obj is not None:
#             return self._wrapped_obj.Name
#
#     @name.setter
#     def name(self, value):
#         if self._wrapped_obj is not None:
#             self._wrapped_obj.Name = value
#
#     @property
#     def layers(self):
#         if self._layers is None:
#             self._layers = self.get_layers()
#         return self._layers
#
#     @property
#     def vertices(self):
#         if self._vertices is None:
#             self._vertices = self.get_vertices()
#         return self._vertices
#
#     @property
#     def edges(self):
#         if self._edges is None:
#             self._edges = self.get_edges()
#         return self._edges
#
#     @property
#     def edge_loops(self):
#         if self._edge_loops is None:
#             self._edge_loops = self.get_edge_loops()
#         return self._edge_loops
#
#     @property
#     def faces(self):
#         if self._faces is None:
#             self._faces = self.get_faces()
#         return self._faces
#
#     @property
#     def volumes(self):
#         if self._volumes is None:
#             self._volumes = self.get_volumes()
#         return self._volumes
#
#     def __getattribute__(self, attr):
#         try:
#             return object.__getattribute__(self, attr)
#         except KeyError:
#             wrapped = object.__getattribute__(self, '_wrapped_obj')
#             if wrapped is not None:
#                 return object.__getattribute__(wrapped, attr)
#             else:
#                 raise KeyError
#
#     def __setattr__(self, attr, value):
#
#         if hasattr(self, '_wrapped_obj'):
#
#             if hasattr(self._wrapped_obj, attr) and (self._wrapped_obj is not None):
#                 object.__setattr__(self._wrapped_obj, attr, value)
#             else:
#                 object.__setattr__(self, attr, value)
#         else:
#             object.__setattr__(self, attr, value)
#
#     def get_vertices(self):
#         return [self.VertexCls(wrapped_obj=x) for x in tqdm(self._wrapped_obj.Geometry.Vertices.Items)]
#
#     def get_edges(self):
#         return [self.EdgeCls(wrapped_obj=x) for x in tqdm(self._wrapped_obj.Geometry.Edges.Items)]
#
#     def get_edge_loops(self):
#         return [self.EdgeLoopCls(wrapped_obj=x) for x in tqdm(self._wrapped_obj.Geometry.EdgeLoops.Items)]
#
#     def get_faces(self):
#         return [self.FaceCls(wrapped_obj=x) for x in tqdm(self._wrapped_obj.Geometry.Faces.Items)]
#
#     def get_volumes(self):
#         return [self.VolumeCls(wrapped_obj=x) for x in tqdm(self._wrapped_obj.Geometry.Volumes.Items)]
#
#     def get_layers(self):
#         return [self.LayerCls(wrapped_obj=x) for x in tqdm(self._wrapped_obj.Geometry.Layers.Items)]
#
#     def get_face_by_id(self, id):
#
#         face = self.FaceCls.get_obj_by_id(id)
#         if face is None:
#             _ = self.faces
#         face = self.FaceCls.get_obj_by_id(id)
#         return face
#
#     def get_zone_by_id(self, id):
#
#         zone = self.VolumeCls.get_obj_by_id(id)
#         if zone is None:
#             _ = self.volumes
#         zone = self.VolumeCls.get_obj_by_id(id)
#         return zone
#
#     def load_all(self):
#
#         logger.info(f'Geometry model: {self.name}: loading vertices')
#         _ = self.vertices
#         logger.info(f'Geometry model: {self.name}: loading edges')
#         _ = self.edges
#         logger.info(f'Geometry model: {self.name}: loading edge loops')
#         _ = self.edge_loops
#         logger.info(f'Geometry model: {self.name}: loading faces')
#         _ = self.faces
#         logger.info(f'Geometry model: {self.name}: loading volumes')
#         _ = self.volumes
#
#         logger.info(f'\n\nGeometry model import info:\n----------------------------------------------')
#         logger.info(f'Geometry model: {self.name}')
#         logger.info(f'Number vertices: {self.vertices.__len__()}')
#         logger.info(f'Number edges: {self.edges.__len__()}')
#         logger.info(f'Number edge_loops: {self.edge_loops.__len__()}')
#         logger.info(f'Number faces: {self.faces.__len__()}')
#         logger.info(f'Number volumes: {self.volumes.__len__()}\n\n')


# def get_obj_by_id(cls, id):
#     return cls._cls_instances_dict.get(id, None)


class BaseGeoBaseClass(object):

    _cls_instances = WeakSet()      # weak set with all created objects
    _create_all = False             # if true all properties are evaluated to create python objects when initialized
    _cls_instances_dict_cache = None

    @classproperty
    def _cls_instances_dict(cls):
        if cls._cls_instances_dict_cache is None:
            cls._cls_instances_dict_cache = dict(zip([x.id for x in cls._cls_instances], [x for x in cls._cls_instances]))
        return cls._cls_instances_dict_cache

    @classmethod
    def get_obj_by_id(cls, id):
        # return cls._cls_instances_dict.get(id, None)
        return get_obj_by_id(cls, id)

    @classproperty
    def cls_instances(cls):
        return list(cls._cls_instances)

    @property
    def name(self):
        if self._wrapped_obj is not None:
            return self._wrapped_obj.Name

    @name.setter
    def name(self, value):
        if self._wrapped_obj is not None:
            self._wrapped_obj.Name = value

    @property
    def id(self):
        return self._wrapped_obj.Id

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        if "_cls_instances" not in cls.__dict__:
            cls._cls_instances = WeakSet()
        try:
            cls._cls_instances.add(instance)
            cls._cls_instances_dict_cache = None
        except Exception as e:
            logger.error(f'Error adding instance {instance} to _cls_instances: {e}')

        return instance

    def __init__(self, *args, **kwargs):
        self.geometry_model = kwargs.get('geometry_model', None)
        self._wrapped_obj = kwargs.get('wrapped_obj', None)

    # @lru_cache(maxsize=None)
    def __getattribute__(self, attr):
        try:
            return object.__getattribute__(self, attr)
        except KeyError:
            wrapped = object.__getattribute__(self, '_wrapped_obj')
            if wrapped is not None:
                return object.__getattribute__(wrapped, attr)
            else:
                raise KeyError

    def __setattr__(self, attr, value):

        if hasattr(self, '_wrapped_obj'):
            if hasattr(self._wrapped_obj, attr) and (self._wrapped_obj is not None):
                object.__setattr__(self._wrapped_obj, attr, value)
            else:
                object.__setattr__(self, attr, value)
                try:
                    object.__getattribute__(self.__class__, attr).fget.cache_clear()
                except AttributeError:
                    pass
        else:
            object.__setattr__(self, attr, value)

    def __del__(self):
        self.__class__._cls_instances_dict_cache = None

    def __repr__(self):
        return f'{self.name}: ' + object.__repr__(self)

    def __getstate__(self):

        logger.warning(f'__getstate__ in experimental state')

        obj_dict = dict()
        for key in dir(self.__class__):
            if type(getattr(self.__class__, key)) is property:
                print(key)
                obj_dict[key] = getattr(self, key)

        return obj_dict

    def __setstate__(self, state):

        logger.warning(f'__setstate__ in experimental state')

        for key, value in state.items():
            try:
                setattr(self, key, value)
            except AttributeError as e:
                pass


class BaseGeometricLayer(BaseGeoBaseClass):

    def __init__(self, *args, **kwargs):
        BaseGeoBaseClass.__init__(self, *args, **kwargs)


class BaseGeometricVertex(BaseGeoBaseClass):

    def __init__(self, *args, **kwargs):
        BaseGeoBaseClass.__init__(self, *args, **kwargs)

    @property
    def position(self):
        wrapped_obj = self._wrapped_obj
        if cs_axis_up == 1:
            return np.array([wrapped_obj.Position.X, wrapped_obj.Position.Y, wrapped_obj.Position.Z])
        elif cs_axis_up == 2:
            return np.array([-wrapped_obj.Position.X, wrapped_obj.Position.Z, wrapped_obj.Position.Y])
        elif cs_axis_up == 3:
            return np.array([wrapped_obj.Position.Y, wrapped_obj.Position.X, wrapped_obj.Position.Z])

    @position.setter
    def position(self, value):
        wrapped_obj = self._wrapped_obj
        if cs_axis_up == 1:
            wrapped_obj.Position.X = value[0]
            wrapped_obj.Position.Y = value[1]
            wrapped_obj.Position.Z = value[2]
        elif cs_axis_up == 2:
            wrapped_obj.Position.X = value[0]
            wrapped_obj.Position.Y = value[2]
            wrapped_obj.Position.Z = value[1]
        elif cs_axis_up == 3:
            wrapped_obj.Position.X = value[1]
            wrapped_obj.Position.Y = value[0]
            wrapped_obj.Position.Z = value[2]


class BaseGeometricEdge(BaseGeoBaseClass):

    def __init__(self, *args, **kwargs):
        BaseGeoBaseClass.__init__(self, *args, **kwargs)
        self._vertices = kwargs.get('vertices', None)

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = self.get_vertices()
        return self._vertices


class BaseGeometricEdgeLoop(BaseGeoBaseClass):

    def __init__(self, *args, **kwargs):
        BaseGeoBaseClass.__init__(self, *args, **kwargs)
        self._edges = kwargs.get('edges', None)

    @property
    def edges(self):
        if self._edges is None:
            self._edges = self.get_edges()
        return self._edges

    @property
    def edge_orientations(self):
        return [x.Orientation for x in self._wrapped_obj.Edges.Items]

    @property
    def points(self):

        points = np.zeros([self.edges.__len__(), 3])

        if self.edge_orientations[0] == 1:
            points[0, :] = self.edges[0].vertices[0].position
        else:
            points[0, :] = self.edges[0].vertices[1].position

        for i, edge in enumerate(self.edges):
            if self.edge_orientations[i] == 1:
                points[i, :] = edge.vertices[1].position
            else:
                points[i, :] = edge.vertices[0].position

        return points


class BaseGeometricFace(BaseGeoBaseClass):

    def __init__(self, *args, **kwargs):
        BaseGeoBaseClass.__init__(self, *args, **kwargs)

    def __repr__(self):
        return f'Face {self.id}: {self.name}'

    @property
    def _components(self):
        return self.geometry_model.get_geo_components(self._wrapped_obj)

    @property
    def components(self):
        return self.geometry_model.get_py_geo_components(self._wrapped_obj)

    @property
    def construction_assignment(self):
        return next((x for x in self._components if x.InstanceType == InstanceType.ALIGNED_WITH), None)

    @property
    def construction(self):
        if self.construction_assignment is None:
            return

        if self.construction_assignment.ReferencedComponents.Items.__len__() == 0:
            return

        component = self.construction_assignment.ReferencedComponents.Items[0].Reference
        return self.geometry_model.template_parser.create_python_object(component, template_name='BuildInConstruction')

    @property
    def normal(self):
        normal = self._wrapped_obj.get_Normal()
        normal_array = np.array([normal.X, normal.Y, normal.Z])
        if cs_axis_up == 1:
            return np.array([normal_array[0],normal_array[1], normal_array[2]])
        elif cs_axis_up == 2:
            return np.array([-normal_array[0], normal_array[2], normal_array[1]])
        elif cs_axis_up == 3:
            return np.array([normal_array[1], normal_array[0], normal_array[2]])

    @property
    def orientation(self):
        return self._wrapped_obj.get_Orientation()

    @property
    def side_1_volume(self):
        volume = None
        if not self._wrapped_obj.PFaces:
            boundary_faces = set(self._wrapped_obj.Boundary.Faces)
            if boundary_faces.__len__() == 2:
                try:
                    boundary_faces.remove(self._wrapped_obj)
                except:
                    pass

                if boundary_faces.__len__() == 1:
                    volume = self.__class__.get_obj_by_id(list(boundary_faces)[0].Id).side_1_volume
        else:
            for p_face in self._wrapped_obj.PFaces:
                if p_face.Orientation == 1:
                    volume = self._wrapped_obj.PFaces[0].Volume
        return volume

    @property
    def side_2_volume(self):
        volume = None
        if not self._wrapped_obj.PFaces:
            boundary_faces = set(self._wrapped_obj.Boundary.Faces)
            if boundary_faces.__len__() == 2:
                try:
                    boundary_faces.remove(self._wrapped_obj)
                except:
                    pass

                if boundary_faces.__len__() == 1:
                    volume = self.__class__.get_obj_by_id(list(boundary_faces)[0].Id).side_2_volume
        else:
            for p_face in self._wrapped_obj.PFaces:
                if p_face.Orientation == -1:
                    volume = self._wrapped_obj.PFaces[0].Volume
        return volume

    @property
    def hull_face(self):
        return None in [self.side_1_volume, self.side_2_volume]


class BaseGeometricVolume(BaseGeoBaseClass):

    def __init__(self, *args, **kwargs):
        BaseGeoBaseClass.__init__(self, *args, **kwargs)
        self._faces = kwargs.get('faces', None)

    @property
    def components(self):
        return self.geometry_model.get_py_geo_components(self._wrapped_obj)


def create_geo_classes(geo_types):
    """
    Create new classes from geometric base classes

    :return:
    """

    logger.debug('creating base geo classes')

    class GeoBaseClass(geo_types['base']):
        pass

    class GeometricLayer(geo_types['layer']):
        pass

    class GeometricVertex(geo_types['vertex']):
        pass

    class GeometricEdge(geo_types['edge']):
        def get_vertices(self):
            return [GeometricVertex.get_obj_by_id(x.Id) for x in self._wrapped_obj.Vertices.Items]

    class GeometricEdgeLoop(geo_types['edge_loop']):
        def get_edges(self):
            return [GeometricEdge.get_obj_by_id(x.Edge.Id) for x in self._wrapped_obj.Edges.Items]

    class GeometricFace(geo_types['face']):

        @property
        def boundary(self):
            return GeometricEdgeLoop.get_obj_by_id(self._wrapped_obj.Boundary.Id)

        @property
        def holes(self):
            return [GeometricEdgeLoop.get_obj_by_id(x.Id) for x in self._wrapped_obj.Holes.Items]

        @property
        def hole_faces(self):
            hole_faces = []
            for hole in self.holes:
                try:
                    hole_face = [x for x in hole._wrapped_obj.Faces if x.Boundary.Id == hole.id][0]
                    hole_faces.append(hole_face)
                except IndexError:
                    logger.warning(f'Face {self.name}, {self.id}: no hole_face found')
                except Exception as e:
                    logger.error(f'Face {self.name}, {self.id}: error evaluating hole faces: {e}')
            return [GeometricFace.get_obj_by_id(x.Id) for x in hole_faces]

        @property
        def points(self):
            return self.boundary.points

    class GeometricVolume(geo_types['volume']):

        def __init__(self, *args, **kwargs):
            geo_types['volume'].__init__(self, *args, **kwargs)
            self._faces = kwargs.get('faces', None)

        @property
        def faces(self):
            if self._faces is None:
                _faces = [GeometricFace.get_obj_by_id(x.Face.Id) for x in self._wrapped_obj.Faces.Items]
                all_faces = copy(_faces)
                [all_faces.extend(x.hole_faces) for x in _faces]
                self._faces = all_faces
            return self._faces

        @faces.setter
        def faces(self, value):
            self._faces = value

    return GeoBaseClass, GeometricLayer, GeometricVertex, GeometricEdge, GeometricEdgeLoop, GeometricFace, GeometricVolume


class BuildInGeoTypes(object):

    def __init__(self):
        self.base = BaseGeoBaseClass
        self.layer = BaseGeometricLayer
        self.vertex = BaseGeometricVertex
        self.edge = BaseGeometricEdge
        self.edge_loop = BaseGeometricEdgeLoop
        self.face = BaseGeometricFace
        self.volume = BaseGeometricVolume


geometry_types = BuildInGeoTypes()
