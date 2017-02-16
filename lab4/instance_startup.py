import time

import boto3
import wget
from boto import ec2
from boto.ec2 import connect_to_region
from boto.ec2.instance import Instance
from os import wait

from boto.manage.cmdshell import sshclient_from_instance

from utilities import read_json


def main():
    config_path = '../aws/conf.json'
    conf = read_json(config_path)
    conn = connect_to_region(conf['region'],
                             aws_access_key_id=conf['aws_access_key'],
                             aws_secret_access_key=conf['aws_secret_access_key'])

    instance = conn.get_all_instances(instance_ids=[conf['instance_id']])[0].instances[0]

    print 'Starting instance'
    start = time.time()
    instance.start()

    print 'Waiting for instance'
    while instance.state != 'running':
        time.sleep(0.1)
        instance.update()
    startup_time = time.time() - start
    print 'Machine running after: %fs' % startup_time

    print 'Creating ssh client'
    ssh_client = sshclient_from_instance(instance,
                                         conf['ssh_key'],
                                         user_name='ubuntu')

    print 'Start apache2'
    status, stdout, _ = ssh_client.run('sudo service apache2 start')
    time.sleep(15)

    print instance.public_dns_name
    url = 'http://%s/index.html' % instance.public_dns_name

    filename = wget.download(url)
    with open(filename, 'r') as f_in:
        text = f_in.read()
    print text


if __name__ == '__main__':
    main()

