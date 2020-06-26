""" Engine-global constants. """

# ---------------------------------------------------
# Environment variable names
# ---------------------------------------------------

ENV_TASK_CLUSTER = 'COWAIT_CLUSTER'
ENV_TASK_DEFINITION = 'COWAIT_TASK'
ENV_GZIP_ENABLED = 'COWAIT_GZIP'


# ---------------------------------------------------
# Container label names
# ---------------------------------------------------

LABEL_TASK_ID = 'cowait/task'
LABEL_PARENT_ID = 'cowait/parent'


# ---------------------------------------------------
# Settings
# ---------------------------------------------------

# Maximum length of environment variables, 100kB
MAX_ENV_LENGTH = 100 * 1024
