
from app import create_app, create_celery

app = create_app()
celery = create_celery(app)


if __name__ == "__main__":
    with app.app_context():
        print("Triggering tasks manually...\n")

        try:
            celery.send_task("delete_unverified_users_older_than", args=(24,))
            print("delete_unverified_users_older_than triggered.")
        except Exception as e:
            print(f"Failed to trigger delete_unverified_users_older_than: {e}")

        try:
            celery.send_task("send_daily_reminders", kwargs={"force_send": True})
            print("send_daily_reminders triggered.")
        except Exception as e:
            print(f"Failed to trigger send_daily_reminders: {e}")

        try:
            celery.send_task("send_monthly_report", kwargs={"force": True})
            print("send_monthly_report triggered.")
        except Exception as e:
            print(f"Failed to trigger send_monthly_report: {e}")

        print("\nAll task trigger attempts complete.")