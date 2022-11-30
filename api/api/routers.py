from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.urls.resolvers import RegexPattern
from typing import OrderedDict
from django.urls import NoReverseMatch, re_path


# show non viewsets routes in "pretty" api root view (like nested routes for example)


class NestedAPIRootView(APIRootView):
    additional_routes = {}
    nested_routes = {}

    def get_view_name(self):
        return "API eFNE"

    def get(self, request, *args, **kwargs):
        data = self.make_url_list(request, self.api_root_dict, *args, **kwargs)
        for key, route in self.nested_routes.items():
            data[key] = self.make_url_list(request, route, *args, **kwargs)
        for name, url in self.additional_routes.items():
            try:
                data[name] = reverse(
                    url, args=args, kwargs=kwargs, request=request)
            except:
                data[name] = request.build_absolute_uri(url)
        return Response(data)

    def make_url_list(self, request, url_dict, *args, **kwargs):
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in url_dict.items():
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get('format')
                )
            except NoReverseMatch as e:
                # Don't bail out if eg. no list routes exist, only detail routes.
                print(e)
                continue
        return ret


class NestedDefaultRouter(DefaultRouter):
    APIRootView = NestedAPIRootView
    nested_routers = {}
    additional_routes = {}

    def register_nested_router(self, key, router):
        self.nested_routers[key] = router

    def register_additional_view(self, key, url):
        self.additional_routes[key] = url

    def get_api_root_view(self, api_urls=None):
        """
        Return a basic root view.
        """
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        nested_routes = {}
        for key, router in self.nested_routers.items():
            nested_routes[key] = {prefix: router.routes[0].name.format(
                basename=basename) for prefix, viewset, basename in router.registry}

        return self.APIRootView.as_view(api_root_dict=api_root_dict, additional_routes=self.additional_routes, nested_routes=nested_routes)

    def get_urls(self):
        ret = super().get_urls()
        # generate urls of nested routers
        for key, router in self.nested_routers.items():
            for url in router.urls:
                # append key at the start of pattern
                if isinstance(url.pattern, RegexPattern):
                    regex = url.pattern._regex
                    new_regex = "^{}/{}".format(key, regex[1:])
                    ret.append(re_path(new_regex, url.callback, name=url.name))
                else:
                    # TODO what if other type of pattern ?
                    ret.append(url)
        return ret
