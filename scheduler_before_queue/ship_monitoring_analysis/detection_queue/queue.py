from celery import Celery
from celery import Task
from celery import bootsteps
from ship_monitoring_analysis.ship_detection_algorithms.ship_detection_mask import predict as predict_module
from ship_monitoring_analysis.utils import csv_utils


celery = Celery('detection_queue',
                broker='pyamqp://guest:12345678@localhost//',
                backend='rpc')


#  Task Inheritance
class PredictionTask(Task):
    model_path = None
    _predictor = None

    @property
    def predictor(self):
        if self._predictor is None:
            self._predictor = predict_module.predictor(self.model_path)
        return self._predictor

    def on_success(self, retval, task_id, args, kwargs):
        prediction_summary_file = kwargs['prediction_summary_file']
        image_id = kwargs['image_id']
        output_path = kwargs['output_path']
        data_dict = {'item_id': [image_id], 'result_path': [output_path]}
        csv_utils.append_new_row(prediction_summary_file, data_dict)


# create task using PredictionTask class
@celery.task(base=PredictionTask, name='predict_task', bind=True)
def predict_task(self, image_id, image_path, output_path, aoi_file, mask_file,
                 detection_date, prediction_summary_file, chunk_size=512, padding_size=128):
    predict_module.main_predict(self.predictor, image_id, image_path, output_path, aoi_file, mask_file,
                                detection_date, chunk_size, padding_size)
    return output_path


# add new worker arguments to celery command line
def add_worker_arguments(parser):
    parser.add_argument(
        '--model-path', dest='model_path', required=True,
        help='Model path.')


celery.user_options['worker'].add(add_worker_arguments)


# assign command line value to PredictionTask class
class MyBootStep(bootsteps.Step):

    def __init__(self, worker, model_path, **options):
        PredictionTask.model_path = model_path


# add MyBootStep to worker
celery.steps['worker'].add(MyBootStep)
