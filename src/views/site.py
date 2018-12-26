from flask import Blueprint, render_template, redirect, url_for, request, flash
from webargs.flaskparser import use_args

from src.common.errors import SiteError
from src.models.site import SiteModel
from src.arguments.argument import Argument

site_blueprint = Blueprint('sites', __name__, template_folder='templates')


@site_blueprint.route('/')
def index():
    try:
        sites = SiteModel.get_sites()
    except SiteError as e:
        return e.message

    return render_template('index.html', sites=sites)


@site_blueprint.route('/purge-site', methods=['POST'])
@use_args(Argument.all_items_in_cache)
def purge_all_items_in_cache(args):
    try:
        site = SiteModel.get_one_site(**args)
        site.purge_all_cache()
    except SiteError as e:
        return e.message

    flash(f'Cache successfully cleared for {site.name}')

    return redirect(url_for('.index'))


@site_blueprint.route('/purge-items', methods=['POST'])
@use_args(Argument.single_items_in_cache)
def purge_single_items_in_cache(args):
    if args['urls'] == '':
        flash('Enter at least one URL')
        return redirect(url_for('.index'))

    try:
        site = SiteModel.get_one_site(args['_id'])
        urls = args['urls'].splitlines()
        purged_urls = site.purge_items_in_cache(urls)

    except SiteError as e:
        return e.message

    if purged_urls:
        flash(f'The following cached files were cleared for {site.name}')
        for url in purged_urls:
            flash(url)
    else:
        flash(f'Cache not purged! No valid urls were entered.')

    return redirect(url_for('.index'))


@site_blueprint.route('/purge-staging', methods=['POST'])
def purge_all_staging_cache():
    try:
        SiteModel.purge_all_staging_cache()
    except SiteError as e:
        return e.message

    flash('Cache successfully cleared for all staging sites')

    return redirect(url_for('.index'))
