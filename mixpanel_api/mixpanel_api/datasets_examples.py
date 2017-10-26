from mixpanel_api import Mixpanel

if __name__ == '__main__':
	credentials = {
		# You can also use a datasets secret here for any version or import function instead
		# For listing or deleting datasets, however, you must use the project API secret
		'API_secret': '',
		'token': '', 
		'project_id': 0
	}


	# In order to import a dataset we must first instantiate a Mixpanel object using either your Mixpanel API secret or 
	# a dataset secret. You also need to provide the dataset name you will be importing into. If you don't know it you can set this later.
	# This object can also be used for exporting or importing other data (see the documentation at X for more information)
	m = Mixpanel(credentials['API_secret'],credentials['token'], dataset_id='test_dataset', project_id=credentials['project_id'])

	# if you don't know the dataset name you wish to use you can retrieve all the datasets 
	all_datasets = m.list_all_datasets()

	# and then set the appropriate dataset, this would set the first one returned. 
	# see the documentation HERE for more information on the response of list_all_datasets
	m.dataset_id = all_datasets[-1]['dataset_id']

	# if you wish to see information for just the current dataset you may do so by 
	current_dataset_information = m.list_dataset()

	m.create_dataset_version()

	# You also need to know which dataset version you wish to work with, or create a new one
	# you may retrieve all of the versions for the dataset currently set on the object by
	all_versions = m.list_all_dataset_versions() 

	# you can easily get the latest version by sorting by created_date
	all_versions.sort(key=lambda version: version['created_at'],reverse=True)
	latest_version = all_versions[0]['version_id']

	# You can then import events by specifying a file that is JSON formatted with an array of Mixpanel events or a CSV of Mixpanel events
	# see HERE for more information on Mixpanel event objects
	m.import_events('test_events', timezone_offset=0, dataset_version=latest_version)


	# You may also import directly from a python object like this example
	test_events = [
							{'event': 'test_event', 'properties' : { 'distinct_id': '123', 'color': 'blue', 'time': 1502427934000, } },
							{'event': 'test_event', 'properties' : { 'distinct_id': '456', 'color': 'red', 'time': 1502427934050, } },
							]

	m.import_events(test_events,timezone_offset=0,dataset_version=latest_version)


	# You can import people in a similar fashion, via a JSON or CSV file, however, you do not need to specify a timezone_offset.
	m.import_people('people_test', dataset_version='5643440998055936')
	
	# Or a list of people objects. You may see HERE for further explanation on people profiles objects
	test_people = [
							{'$distinct_id': '123', '$properties': { '$email' : 'foo@mail.com'}},
							{'$distinct_id': '456', '$properties': { '$email' : 'bar@mail.com'}},
						]

	m.import_people(test_people, dataset_version=latest_version)

	# you may also create a new dataset version if you wish, this will return the current state of the new version
	new_version = m.create_dataset_version()
	m.mark_dataset_version_readable(latest_version)

	# let's wait until this version is ready now
	m.wait_until_dataset_version_ready(latest_version)

	# You can also update a version's state. See HERE for more information on the version object
	m.update_dataset_version(latest_version,{'writable':True, 'readable': False})

	# You can also specifically change the version state to make it readable. This will make this version queryable 
	# in Mixpanel. There can be only one version that is readable at a time so if another version was set to readable previosuly
	# it will subsequently have it's state changed to reflect this
	m.mark_dataset_version_readable(latest_version)

	# You may also delete a specific dataset version as well
	m.delete_dataset_version(latest_version)

	# Or delete an entire dataset to do this you must use the API secret rather than the dataset secret, however.
	m.delete_dataset()
