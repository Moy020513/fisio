from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0005_paciente_ocupacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='antecedentesnopatologicos',
            name='tabaco',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='antecedentesnopatologicos',
            name='alcohol_frecuencia',
            field=models.CharField(choices=[('no', 'No'), ('social', 'Social'), ('diario', 'Diario'), ('regularmente', 'Regularmente')], default='no', max_length=20),
        ),
        migrations.AddField(
            model_name='antecedentesnopatologicos',
            name='azucar_descripcion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
