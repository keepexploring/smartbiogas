class Container(models.Model):
    pass

class ContainerItem(models.Model):
    blog = models.ForeignKey('Container', related_name='items')

# For testing purposes only
class ContainerResource(ModelResource):
    class Meta:
        queryset = Container.objects.all()
        authorization = Authorization()

class ContainerItemResource(ModelResource):
    blog = tastypie.fields.ForeignKey(ContainerResource, 'blog')
    class Meta:
        queryset = ContainerItem.objects.all()
        authorization = Authorization()


class BiogasPlants(models.Model):
    pass

class PendingJobs(models.Model):
    blog = models.ForeignKey('BiogasPlants', related_name='items')

# For testing purposes only
class BiogasPlantResource(ModelResource):
    class Meta:
        queryset = BiogasPlants.objects.all()
        authorization = Authorization()

class PendingJobResource(ModelResource):
    blog = tastypie.fields.ForeignKey(BiogasPlantResource, 'blog')
    class Meta:
        queryset = ContainerItem.objects.all()
        authorization = Authorization()