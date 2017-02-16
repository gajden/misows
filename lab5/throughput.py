import time
from boto.ec2 import connect_to_region
from boto.manage.cmdshell import sshclient_from_instance
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from os.path import getsize

from utilities import read_json


def measure_throughput(key, file_in, file_out):
    print '| > Upload file to s3'
    start = time.time()
    key.set_contents_from_filename(file_in)
    upload_time = time.time() - start
    print '| > time: %fs' % upload_time

    print '| > Get file from s3'
    start = time.time()
    key.get_contents_to_filename(file_out)
    download_time = time.time() - start
    print '| > time: %fs' % download_time

    file_size = getsize(file_in) / 1024 ** 2
    print '| > file size: %f Mb' % file_size
    upload_throughput = file_size / float(upload_time)
    download_throughput = file_size / float(download_time)
    return upload_throughput, download_throughput


def main():
    config_path = '../aws/config.json'
    conf = read_json(config_path)

    conn = S3Connection(conf['aws_access_key'], conf['aws_secret_access_key'])
    bucket = conn.get_bucket(conf['bucket_name'])

    key = Key(bucket)
    key.key = 'test'

    upload, download = measure_throughput(key, '../data/data_1M.dat', '../data/tmp.dat')
    print 'Upload throughput: %f Mb/s' % upload
    print 'Download throughput: %f Mb/s' % download


if __name__ == '__main__':
    main()
