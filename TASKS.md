# Tasks order for rebasing
master -> task-introduce-port-in-items-repository
task-introduce-port-in-items-repository -> task-introduce-port-in-items-repository-with-lagom
master -> task-likes-catalog-direct
task-likes-catalog-direct -> task-likes-catalog-inversed-with-events
task-likes-catalog-inversed-with-events -> task-likes-catalog-inversed-with-events-and-celery-tasks
master -> task-process-manager

