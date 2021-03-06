# Generated by Django 4.0.1 on 2022-01-16 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userApp', '0002_alter_user_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='district',
            field=models.CharField(choices=[('Adilabad', 'Adilabad'), ('Bhadradri Kothagudem', 'Bhadradri Kothagudem'), ('Hanumakonda', 'Hanumakonda'), ('Hyderabad', 'Hyderabad'), ('Jagtial', 'Jagtial'), ('Jangaon', 'Jangaon'), ('Jayashankar Bhupalpally', 'Jayashankar Bhupalpally'), ('Jogulamba Gadwal', 'Jogulamba Gadwal'), ('Kamareddy', 'Kamareddy'), ('Karimnagar', 'Karimnagar'), ('Khammam', 'Khammam'), ('Kumuram Bheem', 'Kumuram Bheem'), ('Mahabubabad', 'Mahabubabad'), ('Mahabubnagar', 'Mahabubnagar'), ('Mancherial', 'Mancherial'), ('Medak', 'Medak'), ('Medchal-Malkajgiri', 'Medchal-Malkajgiri'), ('Mulugu', 'Mulugu'), ('Nagarkurnool', 'Nagarkurnool'), ('Nalgonda', 'Nalgonda'), ('Narayanpet', 'Narayanpet'), ('Nirmal', 'Nirmal'), ('Nizamabad', 'Nizamabad'), ('Peddapalli', 'Peddapalli'), ('Rajanna Sircilla', 'Rajanna Sircilla'), ('Rangareddy', 'Rangareddy'), ('Sangareddy', 'Sangareddy'), ('Siddipet', 'Siddipet'), ('Suryapet', 'Suryapet'), ('Vikarabad', 'Vikarabad'), ('Wanaparthy', 'Wanaparthy'), ('Warangal', 'Warangal'), ('Yadadri Bhuvanagiri', 'Yadadri Bhuvanagiri')], max_length=100),
        ),
    ]
