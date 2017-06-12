
from horizon import forms


class UpdateRbdCacheConfigForm(forms.SelfHandlingForm):
    id = forms.CharField(label="ID", widget=forms.HiddenInput)

    cache_dir = forms.CharField(
        label="cache_dir",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    clean_start = forms.CharField(
        label="clean_start",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    enable_memory_usage_tracker = forms.CharField(
        label="enable_MemoryUsageTracker",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    object_size = forms.CharField(
        label="object_size",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    cache_total_size = forms.CharField(
        label="cache_total_size",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    cache_dirty_ratio_min = forms.CharField(
        label="cache_dirty_ratio_min",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    cache_ratio_health = forms.CharField(
        label="cache_ratio_health",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    cache_ratio_max = forms.CharField(
        label="cache_ratio_max",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    cache_flush_interval = forms.CharField(
        label="cache_flush_interval",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    cache_evict_interval = forms.CharField(
        label="cache_evict_interval",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    cache_flush_queue_depth = forms.CharField(
        label="cache_flush_queue_depth",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    agent_threads_num = forms.CharField(
        label="agent_threads_num",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    cache_service_threads_num = forms.CharField(
        label="cacheservice_threads_num",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    messenger_port = forms.CharField(
        label="messenger_port",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )
    log_to_file = forms.CharField(
        label="log_to_file",
        max_length=255,
        min_length=1,
        error_messages={
            'required': 'This field is required.'
        }
    )

    def handle(self, request, data):
        pass
