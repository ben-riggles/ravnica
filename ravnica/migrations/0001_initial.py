# Generated by Django 4.0.3 on 2022-03-05 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('current', models.BooleanField(default=True)),
                ('content', models.BinaryField()),
            ],
        ),
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('full_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('playoff', models.BooleanField(default=False)),
                ('type', models.IntegerField(choices=[(1, 'Round One'), (2, 'Round Two'), (3, 'Round Three'), (4, 'Round Four'), (5, 'Round Five'), (6, 'Round Six'), (7, 'Round Seven'), (8, 'Round Eight'), (9, 'Round Nine'), (10, 'Semifinals'), (11, 'Finals')])),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ravnica.season')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('away', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deck_away', to='ravnica.deck')),
                ('home', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deck_home', to='ravnica.deck')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ravnica.round')),
                ('winner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deck_winner', to='ravnica.deck')),
            ],
        ),
        migrations.AddField(
            model_name='deck',
            name='guild',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ravnica.guild'),
        ),
    ]
