import json
import worker_system.settings as settings
from django.http import HttpResponse
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from rest_framework.views import APIView

class Store:

    def __init__(self):
        """ initialize the data from the resource """

        self.data_frame = self.get_resource_data()

    def get_resource_data(self):
        """ Fetch the required data from resource file """

        path = settings.PATH
        required_columns = settings.COLUMNS
        spark_ctx = SparkContext.getOrCreate()
        spark = SparkSession(spark_ctx)
        shoes_df = spark.read.csv(path, inferSchema=True, header=True)
        required_df = shoes_df.select(required_columns)
        return required_df

    def get_current_data(self, current_date):
        """ Fetch the data based on the given date """

        data_df = self.data_frame
        date_field = "%{}%".format(current_date)
        recent_items = data_df.filter(data_df.dateAdded.like(date_field))
        return recent_items

class GetRecentItem(APIView):
    """ Return the latest item for the given date """

    def get(self, request):
        """ Get date from request """
        date = request.GET.get('date')
        store = Store()
        recent_items = store.get_current_data(date)
        if recent_items.count():
            item_data = recent_items.orderBy( \
                recent_items.dateAdded, ascending=False \
                ).limit(1)
            recent_item = json.loads(item_data.toJSON().collect()[0])
            res = json.dumps({"status" : "Success", "data" : recent_item})
            return HttpResponse(res)
        res = json.dumps({'status': 'failed', 'error': 'No Data Available'})
        return HttpResponse(res)

class GetBrandCount(APIView):
    """ Return the brand count for the given date """

    def get(self, request):
        """ Get date from request """
        grouped_items = []
        store = Store()
        date = request.GET.get('date')
        selected_items = store.get_current_data(date)
        if selected_items.count():
            grouped_data = selected_items.groupBy('brand').count()\
            .orderBy('count', ascending=False)
            items = grouped_data.toJSON().collect()
            for item in items:
                grouped_items.append(json.loads(item))
            res = json.dumps({"status" : "Success", "data" : grouped_items})
            return HttpResponse(res)
        res = json.dumps({"status" : "failed", "error" : "No Data Available"})
        return HttpResponse(res)

class GetItemsbyColor(APIView):
    """ Return the latest items based on the color """

    def get(self, request):
        """ Get color from request """
        color_items = []
        color = request.GET.get('color')
        store = Store()
        data_df = store.get_resource_data()
        colored_data = data_df.filter(\
            data_df.colors.like(color)).orderBy('dateAdded', ascending=False\
            ).limit(10)
        colored_items = colored_data.toJSON().collect()
        if colored_items:
            for item in colored_items:
                color_items.append(json.loads(item))
            res = json.dumps({"status" : "Success", "data" : color_items})
            return HttpResponse(res)
        res = json.dumps({"status" : "Success", "data" : color_items})
        return HttpResponse(res)
