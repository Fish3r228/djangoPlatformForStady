from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog
from django.urls import reverse_lazy

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj

class BlogCreateView(CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog/blog_form.html'

class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
