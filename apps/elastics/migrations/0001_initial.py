# Generated by Django 2.2.10 on 2021-12-18 13:27

import common.fields.model
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlterWeaken',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False, verbose_name='Is active ')),
                ('frequency', models.IntegerField(blank=True, null=True, verbose_name='Frequency')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'AlterWeaken',
            },
        ),
        migrations.CreateModel(
            name='BreakerConfig',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('fielddata_over', models.CharField(blank=True, max_length=16, null=True, verbose_name='Fielddata overhead')),
                ('request_over', models.CharField(blank=True, max_length=16, null=True, verbose_name='Request overhead')),
                ('total_limit', models.CharField(blank=True, max_length=16, null=True, verbose_name='Total limit')),
                ('request_limit', models.CharField(blank=True, max_length=16, null=True, verbose_name='Request limit')),
                ('fielddata_limit', models.CharField(blank=True, max_length=16, null=True, verbose_name='Fielddata limit')),
                ('inflight_req', models.CharField(blank=True, max_length=16, null=True, verbose_name='Inflight_requests overhead')),
                ('inflight_req_limit', models.CharField(blank=True, max_length=16, null=True, verbose_name='Inflight_requests limit')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('created_by', models.CharField(blank=True, default='', max_length=128, verbose_name='Created by')),
            ],
            options={
                'verbose_name': 'BreakerConfig',
            },
        ),
        migrations.CreateModel(
            name='CloudInfor',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('value', models.CharField(blank=True, max_length=128, null=True, verbose_name='Value')),
                ('key', models.CharField(blank=True, max_length=128, null=True, verbose_name='Key')),
                ('secret', models.CharField(blank=True, max_length=128, null=True, verbose_name='Secret')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, default='', max_length=128, verbose_name='Created by')),
            ],
            options={
                'verbose_name': 'CloudInfor',
                'ordering': ['name'],
                'unique_together': {('org_id', 'name')},
            },
        ),
        migrations.CreateModel(
            name='EsNode',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('uuid', models.CharField(blank=True, max_length=256, null=True, verbose_name='Uuid')),
                ('ip', models.GenericIPAddressField(db_index=True, verbose_name='IP')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('disktotal', models.BigIntegerField(verbose_name='Disk total')),
                ('diskused', models.BigIntegerField(verbose_name='Disk used')),
                ('diskavail', models.BigIntegerField(verbose_name='Disk avail')),
                ('ramcurrent', models.BigIntegerField(verbose_name='Used total memory')),
                ('rammax', models.BigIntegerField(verbose_name='Total memory')),
                ('noderole', models.CharField(db_index=True, max_length=64, verbose_name='Node roles')),
                ('pid', models.IntegerField(verbose_name='Process id')),
                ('port', models.IntegerField(verbose_name='Transmission port')),
                ('http_address', models.CharField(blank=True, db_index=True, max_length=64, verbose_name='Http monitoring')),
                ('version', models.CharField(max_length=64, verbose_name='Version')),
                ('jdk', models.CharField(db_index=True, max_length=64, verbose_name='Jdk version')),
                ('uptime', models.CharField(db_index=True, max_length=64, verbose_name='Running uptime')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
            ],
            options={
                'verbose_name': 'EsNode',
                'ordering': ['ip'],
            },
        ),
        migrations.CreateModel(
            name='Index',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_index=True, max_length=256, null=True, verbose_name='Name')),
                ('uuid', models.CharField(blank=True, max_length=256, null=True, verbose_name='Uuid')),
                ('pri', models.CharField(blank=True, max_length=256, null=True, verbose_name='Primary shard')),
                ('rep', models.IntegerField(blank=True, null=True, verbose_name='Replica Set')),
                ('dc', models.BigIntegerField(blank=True, null=True, verbose_name='Total docs')),
                ('ssize', models.BigIntegerField(blank=True, null=True, verbose_name='Store size')),
                ('pss', models.BigIntegerField(blank=True, null=True, verbose_name='Pri store size')),
                ('health', models.CharField(max_length=32, verbose_name='Health')),
                ('status', models.CharField(max_length=32, verbose_name='Status')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
            ],
            options={
                'verbose_name': 'Index',
                'ordering': ['-date_updated'],
            },
        ),
        migrations.CreateModel(
            name='MetaInfo',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_index=True, max_length=64, null=True, verbose_name='Name')),
                ('env', models.CharField(choices=[('dev', 'dev'), ('test', 'test'), ('uat', 'uat'), ('pre', 'pre'), ('gra', 'gra'), ('prd', 'prd')], default='', max_length=32, verbose_name='Env')),
                ('address', models.CharField(blank=True, db_index=True, max_length=512, null=True, verbose_name='Address')),
                ('username', models.CharField(blank=True, max_length=128, null=True, verbose_name='Username')),
                ('password', models.CharField(blank=True, max_length=128, null=True, verbose_name='Password')),
                ('kibana', models.URLField(blank=True, max_length=512, null=True, verbose_name='Kibana addr')),
                ('kafka', models.URLField(blank=True, max_length=512, null=True, verbose_name='Kafka addr')),
                ('health', models.BooleanField(default=True, verbose_name='Health')),
                ('setting', models.BooleanField(default=False, verbose_name='Setting ')),
                ('alter', models.BooleanField(default=False, verbose_name='Alter')),
                ('indexes', models.BooleanField(default=False, verbose_name='Index')),
                ('node', models.BooleanField(default=True, verbose_name='Node')),
                ('remote', models.BooleanField(default=False, verbose_name='Remote cluster')),
                ('scbcl', models.BooleanField(default=False, verbose_name='Sync across clusters')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('labels', models.CharField(blank=True, max_length=32, null=True, verbose_name='Labels')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('created_by', models.CharField(blank=True, default='', max_length=128, verbose_name='Created by')),
                ('cloud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cloudinfor', to='elastics.CloudInfor', verbose_name='Cloud')),
            ],
            options={
                'verbose_name': 'MetaInfo',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RoutingConfig',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('rebalance_enable', models.CharField(blank=True, max_length=16, null=True, verbose_name='Rebalance enable')),
                ('node_concurrent_recoveries', models.IntegerField(blank=True, null=True, verbose_name='Node concurrent recoveries')),
                ('cluster_concurrent_rebalance', models.IntegerField(blank=True, null=True, verbose_name='Cluster concurrent rebalance')),
                ('node_initial_primaries_recoveries', models.IntegerField(blank=True, null=True, verbose_name='Node initial primaries recoveries')),
                ('node_concurrent_outgoing_recoveries', models.IntegerField(blank=True, null=True, verbose_name='Node concurrent outgoing recoveries')),
                ('disk_watermark_flood_stage', models.CharField(blank=True, max_length=16, null=True, verbose_name='Disk watermark flood stage')),
                ('disk_watermark_low', models.CharField(blank=True, max_length=16, null=True, verbose_name='Disk watermark low')),
                ('disk_watermark_high', models.CharField(blank=True, max_length=16, null=True, verbose_name='Disk watermark high')),
                ('allow_rebalance', models.CharField(blank=True, max_length=32, null=True, verbose_name='Allow rebalance')),
                ('allocation_enable', models.CharField(blank=True, max_length=16, null=True, verbose_name='Allocation enable')),
                ('awareness_attributes', models.CharField(blank=True, max_length=16, null=True, verbose_name='Awareness attributes')),
                ('balance_index', models.CharField(blank=True, max_length=16, null=True, verbose_name='Balance index')),
                ('balance_threshold', models.CharField(blank=True, max_length=16, null=True, verbose_name='Balance threshold')),
                ('balance_shard', models.CharField(blank=True, max_length=16, null=True, verbose_name='Balance shard')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('created_by', models.CharField(blank=True, default='', max_length=128, verbose_name='Created by')),
                ('metainfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.MetaInfo', verbose_name='Metainfo')),
            ],
            options={
                'verbose_name': 'RoutingConfig',
            },
        ),
        migrations.CreateModel(
            name='RoutingConfigNum',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('metainfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.MetaInfo', verbose_name='Metainfo')),
                ('routingConfig', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.RoutingConfig', verbose_name='RoutingConfig')),
            ],
            options={
                'verbose_name': 'RoutingConfigNum',
            },
        ),
        migrations.CreateModel(
            name='NodeFs',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('path', models.CharField(blank=True, max_length=512, null=True, verbose_name='Data path')),
                ('mount', models.CharField(blank=True, max_length=512, null=True, verbose_name='Mount path')),
                ('filesystem', models.CharField(max_length=64, null=True, verbose_name='File system')),
                ('total', models.BigIntegerField(verbose_name='Total size')),
                ('free', models.BigIntegerField(verbose_name='Free size')),
                ('available', models.BigIntegerField(verbose_name='Available')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('esnode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.EsNode', verbose_name='Esnode')),
            ],
            options={
                'verbose_name': 'NodeFs',
            },
        ),
        migrations.CreateModel(
            name='IndiceShard',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('shard', models.IntegerField(null=True, verbose_name='Shard')),
                ('pr', models.CharField(choices=[('p', 'Primary'), ('r', 'Replica')], max_length=32, null=True, verbose_name='Primary or Replica')),
                ('st', models.CharField(choices=[('INITIALIZING', 'The shard is recovering from a peer shard or gateway.'), ('RELOCATING', 'The shard is relocating.'), ('STARTED', 'The shard has started.'), ('UNASSIGNED', 'The shard is not assigned to any node.')], max_length=128, null=True, verbose_name='State')),
                ('dc', models.BigIntegerField(blank=True, null=True, verbose_name='Shard docs')),
                ('sto', models.BigIntegerField(blank=True, null=True, verbose_name='Shard store size(GB)')),
                ('uid', models.CharField(blank=True, max_length=128, null=True, verbose_name='Uid')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('esnode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.EsNode', verbose_name='Esnode')),
                ('index', models.ManyToManyField(to='elastics.Index', verbose_name='Index')),
            ],
            options={
                'verbose_name': 'IndiceShard',
                'ordering': ['-date_updated'],
            },
        ),
        migrations.CreateModel(
            name='IndiceNode',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('refresh', models.IntegerField(verbose_name='Refresh')),
                ('flush', models.IntegerField(verbose_name='Flush')),
                ('recovery', models.IntegerField(verbose_name='Recovery')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('esnode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.EsNode', verbose_name='Esnode')),
                ('index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.Index', verbose_name='Index')),
            ],
            options={
                'verbose_name': 'IndiceNode',
                'ordering': ['esnode'],
            },
        ),
        migrations.AddField(
            model_name='index',
            name='metainfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.MetaInfo', verbose_name='Metainfo'),
        ),
        migrations.AddField(
            model_name='esnode',
            name='metainfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.MetaInfo', verbose_name='Metainfo'),
        ),
        migrations.CreateModel(
            name='ClusterSetting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('persis', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Permanent parameters')),
                ('tran', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Temporary parameters')),
                ('def_clus', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Default cluster parameters')),
                ('def_xpack', jsonfield.fields.JSONField(blank=True, null=True, verbose_name='Security')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('metainfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.MetaInfo', verbose_name='Metainfo')),
            ],
            options={
                'verbose_name': 'ClusterSetting',
                'ordering': ['-date_updated'],
            },
        ),
        migrations.CreateModel(
            name='ClusterRemote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Name')),
                ('mode', models.CharField(blank=True, max_length=16, null=True, verbose_name='Connection mode')),
                ('conn', models.CharField(blank=True, max_length=16, null=True, verbose_name='Status')),
                ('conn_timeout', models.CharField(blank=True, max_length=16, null=True, verbose_name='Connection timed out')),
                ('skip_una', models.CharField(blank=True, max_length=16, null=True, verbose_name='Skip cluster')),
                ('seeds', models.TextField(blank=True, null=True, verbose_name='Connection address')),
                ('num_nodes', models.CharField(blank=True, max_length=16, null=True, verbose_name='Number of nodes')),
                ('max_conn', models.CharField(blank=True, max_length=16, null=True, verbose_name='Maximum connection')),
                ('proxy_add', models.CharField(blank=True, max_length=128, null=True, verbose_name='Proxy model')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('metainfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.MetaInfo', verbose_name='Metainfo')),
            ],
            options={
                'verbose_name': 'ClusterRemote',
                'ordering': ['-date_updated'],
            },
        ),
        migrations.CreateModel(
            name='BreakerConfigNum',
            fields=[
                ('org_id', models.CharField(blank=True, db_index=True, default='', max_length=36, verbose_name='Organization')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('breakerconfig', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.BreakerConfig', verbose_name='BreakerConfig')),
                ('metainfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.MetaInfo', verbose_name='Metainfo')),
            ],
            options={
                'verbose_name': 'BreakerConfigNum',
            },
        ),
        migrations.AddField(
            model_name='breakerconfig',
            name='metainfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.MetaInfo', verbose_name='Metainfo'),
        ),
        migrations.CreateModel(
            name='BasicCluster',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_index=True, max_length=64, null=True, verbose_name='Name')),
                ('status', models.CharField(blank=True, max_length=64, null=True, verbose_name='Status')),
                ('st', models.IntegerField(blank=True, null=True, verbose_name='Total shard')),
                ('sp', models.IntegerField(blank=True, null=True, verbose_name='Primary shard')),
                ('incount', models.IntegerField(blank=True, null=True, verbose_name='Total index')),
                ('indocs', models.BigIntegerField(blank=True, null=True, verbose_name='Total docs')),
                ('instore', models.BigIntegerField(blank=True, null=True, verbose_name='Total use space')),
                ('nt', models.IntegerField(blank=True, null=True, verbose_name='Total node')),
                ('nc', models.IntegerField(blank=True, null=True, verbose_name='Read-only node')),
                ('nd', models.IntegerField(blank=True, null=True, verbose_name='Data node')),
                ('ni', models.IntegerField(blank=True, null=True, verbose_name='Ingest node')),
                ('nm', models.IntegerField(blank=True, null=True, verbose_name='Master node')),
                ('nr', models.IntegerField(blank=True, null=True, verbose_name='Client node')),
                ('mt', models.BigIntegerField(blank=True, null=True, verbose_name='Total memory')),
                ('mf', models.BigIntegerField(blank=True, null=True, verbose_name='Free memory')),
                ('mu', models.BigIntegerField(blank=True, null=True, verbose_name='Use memory')),
                ('pt', common.fields.model.JsonDictTextField(blank=True, null=True, verbose_name='Install')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date updated')),
                ('metainfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.MetaInfo', verbose_name='Metainfo')),
            ],
            options={
                'verbose_name': 'BasicCluster',
                'ordering': ['name'],
            },
        ),
    ]
