class ModelMovieListMixin:
    model = None

    def get_queryset(self):
        model_url = f'{self.model.__name__.lower()}_url'
        model_instance = self.model.objects.get(url=self.kwargs[model_url])
        self.kwargs['title'] = model_instance.name
        return model_instance.movies.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['title']
        return context