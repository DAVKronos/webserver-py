# TO RUN THIS FILE  : docker compose run --rm python python3 -m app.data_migration.main

import asyncio
from datetime import datetime
from sqlalchemy import text
from ..database import create_ssh_engine
import app.data_migration.migration_helper as helper

async def empty_db(conn):
    # Empty the new database first
    print("Emptying the new database...")
    await conn.execute(text("""
        TRUNCATE 
            agendaitem_types, committees, files, mail_aliases, pages, 
            photo_tags, user_types, document_folders, documents, 
            mailing_lists, users, agendaitems, committee_members, 
            mailing_list_members, photo_albums, photos, 
            reset_password_actions, subscriptions, announcements, 
            has_tag, news_items, news_comments 
        RESTART IDENTITY CASCADE;
    """))
    print("Database cleared.")

async def migrate(old_conn, new_conn):
    await empty_db(new_conn)

    # photo_tags_mapping = {
    #     "id": "id",
    #     "name": "name"
    # }
    # await helper.migrate_table(old_conn, new_conn, "tag_", "photo_tags", photo_tags_mapping)

    pages_mapping = {
        "id": "id",
        "information": "content_nl",
        "information_en": "content_en",
        "pagetag": "page_title_nl",
        "pagetag_en": "page_title_en",
        "menu": "menu_item",
        "highlight": "is_highlight",
        "public": "is_public",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    await helper.migrate_table(old_conn, new_conn, "pages", "pages", pages_mapping)

    mail_alias_mapping = {
        "id": "id",
        "name": "name",
        "emailaddress": "email_address",
        "description": "description",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    await helper.migrate_table(old_conn, new_conn, "aliases", "mail_aliases", mail_alias_mapping)

    user_types_mapping = {
        "id": "id", 
        "name": "name_nl", 
        "name_en": "name_en", 
        "donor": "is_donor", 
        "competition": "is_competition", 
        "created_at": "created_at", 
        "updated_at": "updated_at"
    }
    await helper.migrate_table(old_conn, new_conn, "user_types", "user_types", user_types_mapping)

    agendaitems_types_mapping = {
        "id": "id", 
        "name": "name_nl", 
        "name_en": "name_en", 
        "created_at": "created_at", 
        "updated_at": "updated_at"
    }
    await helper.migrate_table(old_conn, new_conn, "agendaitemtypes", "agendaitem_types", agendaitems_types_mapping)
    
    committees_mapping = {
        "id": "id", 
        "name": "name_nl", 
        "name_en": "name_en", 
        "description": "description_nl", 
        "description_en": "description_en", 
        "email": "email", 
        "role": "role", 
        "created_at": "created_at", 
        "updated_at": "updated_at"
    }
    await helper.migrate_table(old_conn, new_conn, "commissions", "committees", committees_mapping)

    user_mapping = {
        "id": 'id',
        "name": 'name',
        "initials": 'initials',
        "email": 'email',
        "encrypted_password": "password",
        "birthdate": 'birthdate',
        "address": 'address',
        "postalcode": 'postalcode',
        "city": 'city',
        "sex": 'sex',
        "allow_password_change": 'allow_password_change',
        "phonenumber": 'phonenumber',
        "user_type_id": 'user_type_id', 
        "bank_account_number": 'bank_account_number',
        "xtracard": 'unioncard_number',
        "instelling": 'institution',
        "aanvang": 'joined_in',
        "tokens": 'tokens',
        "confirmed_at": 'confirmed_at',
        "created_at": 'created_at' or datetime.now(),
        "updated_at": 'updated_at' or datetime.now()
    }
    await helper.migrate_table(old_conn, new_conn, "users", "users", user_mapping, {}, helper.user_criteria, exclude_ids=[479])

    announcement_mapping = {
        "id": "id",
        "title": "title",
        "message": "content",
        "user_id": "user_id",
        "url": "url",
        "starts_at": "starts_at",
        "ends_at": "ends_at",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    announcement_fk_mapping = {
        "user_id": "users"
    }
    await helper.migrate_table(old_conn, new_conn, "announcements", "announcements", announcement_mapping, announcement_fk_mapping)

    mailing_list_mapping = {
        "id": "id",
        "name": "name",
        "description": "description",
        "address": "email_address",
        "local_part": "local_part",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    await helper.migrate_table(old_conn, new_conn, "mailinglists", "mailing_lists", mailing_list_mapping)

    mailing_list_members_mapping = {
        "id": "id",
        "mailinglist_id": "mailing_list_id",
        "user_id": "user_id",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    mailing_list_members_fk_mapping = {
        "mailing_list_id": "mailing_lists",
        "user_id": "users"
    }
    await helper.migrate_table(old_conn, new_conn, "mailinglist_memberships", "mailing_list_members", mailing_list_members_mapping, mailing_list_members_fk_mapping)

    committee_members_map = {
        "id": "id",
        "function": "function",
        "user_id": "user_id",
        "commission_id": "committee_id",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    committee_members_fk_map = {
        "user_id": "users",
        "committee_id": "committees"
    }
    await helper.migrate_table(old_conn, new_conn, "commission_memberships", "committee_members", committee_members_map, committee_members_fk_map)

    agenda_items_mapping = {
        "id": "id",
        "name": "name_nl",
        "name_en": "name_en",
        "description": "description_nl",
        "description_en": "description_en",
        "date": "date",
        "location": "location",
        "commission_id": "committee_id",
        "intern": "is_internal",
        "agendaitemtype_id": "agendaitem_type_id",
        "url": "url",
        "user_id": "created_by_user_id",
        "subscribe": "can_subscribe",
        "subscriptiondeadline": "subscription_deadline",
        "maxsubscription": "max_subscriptions",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    agenda_items_fk_mapping = {
        "committee_id": "committees",
        "agendaitem_type_id": "agendaitem_types",
        "created_by_user_id": "users"
    }
    await helper.migrate_table(old_conn, new_conn, "agendaitems", "agendaitems", agenda_items_mapping, agenda_items_fk_mapping)

    news_items_mapping = {
        "id": "id",
        "title": "title_nl",
        "title_en": "title_en",
        "news": "content_nl",
        "news_en": "content_en",
        "agreed": "approved",
        "agreed_by": "approved_by",
        "user_id": "creator_id",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    news_items_fk_mapping = {
        "approved_by": "users",
        "creator_id": "users"
    }
    await helper.migrate_table(old_conn, new_conn, "newsitems", "news_items", news_items_mapping, news_items_fk_mapping)

    news_comments_mapping = {
        "id": "id",
        "user_id": "user_id",
        "newsitem_id": "newsitem_id",
        "commenttext": "content",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    news_comments_fk_mapping = {
        "user_id": "users",
        "newsitem_id": "news_items"
    }
    await helper.migrate_table(old_conn, new_conn, "comments", "news_comments", news_comments_mapping, news_comments_fk_mapping)

    subscription_mapping = {
        "id": "id",
        "user_id": "user_id",
        "comment": "comment",
        "agendaitem_id": "agendaitem_id",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    subscription_fk_mapping = {
        "user_id": "users",
        "agendaitem_id": "agendaitems"
    }
    await helper.migrate_table(old_conn, new_conn, "subscriptions", "subscriptions", subscription_mapping, subscription_fk_mapping)
    
    photo_album_mapping = {
        "id": "id",
        "name": "name_nl",
        "name_en": "name_en",
        "agendaitem_id": "agendaitem_id",
        "public": "is_public",
        "event_date": "event_date",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    photo_album_fk_mapping = {
        "agendaitem_id": "agendaitems"
    }
    await helper.migrate_table(old_conn, new_conn, "photoalbums", "photo_albums", photo_album_mapping, photo_album_fk_mapping)

    document_folder_mapping = {
        "id": "id",
        "name": "name",
        "folder_id": "parent_folder_id"
    }
    await helper.migrate_self_referencing_table(old_conn, new_conn, "folders", "document_folders", document_folder_mapping, "parent_folder_id")

    document_mapping = {
        "id": "id",
        "name": "name",
        "date": "date",
        "folder_id": "folder_id",
        "public": "is_public",
        "created_at": "created_at",
        "updated_at": "updated_at"
    }
    await helper.migrate_table(old_conn, new_conn, "kronometers", "documents", document_mapping)

    user_avatar_field_names = {
        "path": "avatar_file_name",
        "content_type": "avatar_content_type",
        "file_size": "avatar_file_size",
        "updated_at": "avatar_updated_at"
    }
    await helper.migrate_table_file(old_conn, new_conn, "users", "users", user_avatar_field_names, "avatar_file_id", "/static/avatars/")

    newsitem_file_field_names = {
        "path": "articlephoto_file_name",
        "content_type": "articlephoto_content_type",
        "file_size": "articlephoto_file_size",
        "updated_at": "articlephoto_updated_at"
    }
    await helper.migrate_table_file(old_conn, new_conn, "newsitems", "news_items", newsitem_file_field_names, "photo_file_id", "/static/newsitems/")

    announcement_file_field_names = {
        "path": "background_file_name",
        "content_type": "background_content_type",
        "file_size": "background_file_size",
        "updated_at": "background_updated_at"
    }
    await helper.migrate_table_file(old_conn, new_conn, "announcements", "announcements", announcement_file_field_names, "photo_file_id", "/static/announcements/")

    document_file_field_names = {
        "path": "file_file_name",
        "content_type": "file_content_type",
        "file_size": "file_file_size",
        "updated_at": "file_updated_at"
    }
    await helper.migrate_table_file(old_conn, new_conn, "kronometers", "documents", document_file_field_names, "file_id", "/static/documents/")

    # A lot of refs are now invalid because the photoalbums table in the test database has been whiped,
    # so there are a lot of photos missing. This will be different on the prod database
    await helper.migrate_photos(old_conn, new_conn)

    
    print("Finished migration.")

# Setup dual connection
async def run_with_dual_connection(func, old_db_name, new_db_name):
    with create_ssh_engine(old_db_name) as old_engine, \
         create_ssh_engine(new_db_name) as new_engine:
        async with old_engine.connect() as old_conn:
            async with new_engine.connect() as new_conn:
                await func(old_conn, new_conn)
                await new_conn.commit()

# Start migration
if __name__ == "__main__":
    print("""
It is EXTREMELY important that your config.toml references the correct databases.  
    > database_old    should be referring to the db FROM which the migration happens.
    > database        should be referring to the db TO which the migration happens.
!! This database will be EMPTIED before migration starts. !!
Have you checked your config and are you sure to continue? [Y/N]
          """)
    res = str(input())
    if (res == "Y"):
        asyncio.run(run_with_dual_connection(migrate, 'database_old', 'database'))