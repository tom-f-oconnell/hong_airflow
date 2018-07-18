#!/usr/bin/env python3

# Airflow DAG to describe...
"""
Transfer of acquisition output from original computers, to storage and analysis
machines for tracking and downstream steps.
"""

from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    # TODO need an owner? what do i want?
    # what does depends_on_past do?
    # TODO way to make unlimited? 
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# __file__? guess it shouldn't change (but really less often than filename?)
# example uses schedule_interval. what is default? requiring manual triggering?
# TODO want concurrency limit, but only wrt same input. way to achieve?
# necessary? (also, is default concurrency actually 16? don't want that kind of
# limit across all instantiations with diff input)
with DAG('offline_tracking',
         default_args=default_args,
         # is None or '@once' more appropriate?
         schedule_interval=None,
         # TODO some way to make start_date not necessary? all/most DAGs should
         # run once and start as soon as possible in my case, so it doesn't
         # really make sense
         start_date=datetime.now() - timedelta(days=2),
         description=__doc__) as dag:

    t1 = BashOperator(
        task_id='print_date',
        bash_command='date')

    t2 = BashOperator(
        task_id='sleep',
        bash_command='sleep 5',
        retries=3)

    templated_command = """
	 {% for i in range(5) %}
	     echo "{{ ds }}"
	     echo "{{ macros.ds_add(ds, 7)}}"
	     echo "{{ params.my_param }}"
	 {% endfor %}
	"""

    t3 = BashOperator(
	task_id='templated',
	bash_command=templated_command,
	params={'my_param': 'Parameter I passed in'},
	dag=dag) 

    t1 >> t2
    t1 >> t3

