# Tasks order for rebasing
master -> task-introduce-port-in-items-repository

task-introduce-port-in-items-repository -> task-introduce-port-in-items-repository-with-lagom

master -> task-likes-catalog-direct

task-likes-catalog-direct -> task-likes-catalog-inversed-with-events

task-likes-catalog-inversed-with-events -> task-likes-catalog-inversed-with-events-and-celery-tasks

master -> task-process-manager

master -> design-patterns

design-patterns -> design-patterns-negotiations-phase-1

design-patterns-negotiations-phase-1 -> design-patterns-negotiations-phase-2

design-patterns-negotiations-phase-2 -> design-patterns-negotiations-phase-3

design-patterns-negotiations-phase-3 -> design-patterns-negotiations-state

design-patterns-negotiations-phase-3 -> design-patterns-negotiations-strategies

design-patterns-negotiations-phase-3 -> design-patterns-negotiations-app
