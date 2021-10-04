from __future__ import annotations
import typing


class AnnotationWrapper:
    def __init__(self, class_object: typing.Type):
        self.class_object = class_object
        self._annotations = None

    def __getitem__(self, name) -> AnnotationWrapperGetter:
        return AnnotationWrapperGetter(name, self)

    @property
    def annotations(self):
        if self._annotations is None:
            self._annotations = typing.get_type_hints(self.class_object)
        return self._annotations

    def get(self, name):
        return self.annotations[name]


class AnnotationWrapperGetter:
    def __init__(self, name: str, wrapper: AnnotationWrapper):
        self.name = name
        self.wrapper = wrapper

    def get(self):
        return self.wrapper.get(self.name)
