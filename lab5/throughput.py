import time
from boto.ec2 import connect_to_region
from boto.manage.cmdshell import sshclient_from_instance
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from utilities import read_json


def measure_throughput_from_e2(conf, key, key_str, filename):
    print 'Measure throughput from ec2 instance.'
    config_path = '../aws/conf.json'
    conf = read_json(config_path)
    conn = connect_to_region(conf['region'],
                             aws_access_key_id=conf['aws_access_key'],
                             aws_secret_access_key=conf['aws_secret_access_key'])

    instance = conn.get_all_instances(instance_ids=[conf['instance_id']])[0].instances[0]

    print '| >Starting instance'
    start = time.time()
    instance.start()

    print '| > Waiting for instance'
    while instance.state != 'running':
        time.sleep(1.0)
        instance.update()

    print '| > rCreating ssh client'
    ssh_client = sshclient_from_instance(instance,
                                         conf['ssh_key'],
                                         user_name='ubuntu')

    print 'Start apache2'
    status, stdout, _ = ssh_client.run('sudo service apache2 start')
    time.sleep(15)

    print instance.public_dns_name
    url = 'http://%s/index.html' % instance.public_dns_name
    pass


def measure_throughput(key, key_str, filename):

    pass


def main():
    config_path = '../aws/conf.json'
    conf = read_json(config_path)

    conn = S3Connection(conf['aws_access_key'], conf['aws_secret_access_key'])
    bucket = conn.get_bucket(conf['bucket_name'])

    key = Key(bucket)



