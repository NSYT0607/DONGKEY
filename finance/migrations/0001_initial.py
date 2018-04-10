# Generated by Django 2.0.1 on 2018-02-19 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('club', '0010_auto_20180214_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='club.Club')),
            ],
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='분류명')),
            ],
        ),
        migrations.CreateModel(
            name='Expenditure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(max_length=500, null=True, verbose_name='지출 내역')),
                ('amount', models.IntegerField(blank=True, null=True, verbose_name='지출 금액')),
                ('expd_at', models.DateField(blank=True, null=True)),
                ('receipt', models.ImageField(blank=True, null=True, upload_to='expenditure/%Y/%m/%d/')),
                ('accounting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.Accounting')),
                ('classfication', models.ManyToManyField(blank=True, to='finance.Classification')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(max_length=500, null=True, verbose_name='수입 내역')),
                ('amount', models.IntegerField(blank=True, null=True, verbose_name='수입 금액')),
                ('income_at', models.DateField(blank=True, null=True)),
                ('accounting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.Accounting')),
                ('classfication', models.ManyToManyField(blank=True, to='finance.Classification')),
            ],
        ),
    ]