import csv
import datetime

from django.contrib import admin
from django.contrib.admin import util as admin_util
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse


def export_model_as_csv(modeladmin, request, queryset):
    if hasattr(modeladmin, 'exportable_fields'):
        field_list = modeladmin.exportable_fields
    else:
        # Copy modeladmin.list_display to remove action_checkbox
        field_list = modeladmin.list_display[:]

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s-%s-export-%s.csv' % (
        __package__.lower(),
        queryset.model.__name__.lower(),
        datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    writer = csv.writer(response)
    writer.writerow(
        [admin_util.label_for_field(f, queryset.model, modeladmin) for f in field_list],
    )

    for obj in queryset:
        csv_line_values = []
        for field in field_list:
            field_obj, attr, value = admin_util.lookup_field(field, obj, modeladmin)
            csv_line_values.append(value)

        writer.writerow(csv_line_values)

    return response
export_model_as_csv.short_description = _('Export to CSV')

