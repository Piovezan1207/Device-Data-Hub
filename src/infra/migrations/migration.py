def upgrade():
    # Create the robots table
    op.create_table(
        'robots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=128), nullable=False),
        sa.Column('axis', sa.Integer(), nullable=False),
        sa.Column('brand', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create the connections table
    op.create_table(
        'connections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('robot_id', sa.Integer(), nullable=False),
        sa.Column('topic', sa.String(length=128), nullable=False),
        sa.Column('ip', sa.String(length=15), nullable=False),
        sa.Column('port', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(length=256), nullable=True),
        sa.Column('number', sa.String(length=64), nullable=True),
        sa.Column('password', sa.String(length=128), nullable=True),
        sa.ForeignKeyConstraint(['robot_id'], ['robots.id']),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop the connections table
    op.drop_table('connections')

    # Drop the robots table
    op.drop_table('robots')
