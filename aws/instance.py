import boto
from boto.ec2 import connect_to_region

from utilities import read_json

boto.set_stream_logger('boto')


class Instance(object):
    def __init__(self, conf):
        self.conf = read_json(conf)
        self.conn = connect_to_region(self.conf['region'],
                                      aws_access_key=self.conf[''],
                                      aws_secret_access_key=self.conf[''])

    def start(self):
        self.conn.run_instances(self.conf['ami_image_id'],
                                key_name=self.conf['key_name'],
                                instance_type=self.conf['instance_type'],
                                security_groups=self.conf['security_groups'])

    def stop(self):
        self.conn.stop_instances([])

    def get_id(self):
        pass

