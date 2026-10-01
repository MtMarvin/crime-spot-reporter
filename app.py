
from flask import Flask, render_template, request, redirect, url_for
import os
import re
from datetime import datetime
from html import escape
from werkzeug.utils import secure_filename


# ============================================================
# APPLICATION
# ============================================================

app = Flask(__name__)

# Maximum total request size:
# 50 MB per submission, including uploaded evidence.
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024


# ============================================================
# FOLDERS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SUBMISSIONS_FOLDER = os.path.join(
    BASE_DIR,
    "submissions"
)

UPLOADS_FOLDER = os.path.join(
    SUBMISSIONS_FOLDER,
    "uploads"
)

os.makedirs(SUBMISSIONS_FOLDER, exist_ok=True)
os.makedirs(UPLOADS_FOLDER, exist_ok=True)


# ============================================================
# ALLOWED EVIDENCE FILE TYPES
# ============================================================

ALLOWED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp"
}

ALLOWED_VIDEO_EXTENSIONS = {
    "mp4",
    "mov",
    "avi",
    "webm",
    "m4v"
}

ALLOWED_EVIDENCE_EXTENSIONS = (
    ALLOWED_IMAGE_EXTENSIONS |
    ALLOWED_VIDEO_EXTENSIONS
)


# ============================================================
# CATEGORY CONFIGURATION
# ============================================================

CATEGORY_ROUTES = {
    "theft": {
        "name": "Theft",
        "template": "theft.html"
    },

    "burglary": {
        "name": "Housebreaking / Burglary",
        "template": "burglary.html"
    },

    "robbery": {
        "name": "Robbery",
        "template": "robbery.html"
    },

    "assault": {
        "name": "Assault",
        "template": "assault.html"
    },

    "sexual-offence": {
        "name": "Sexual Offence",
        "template": "sexual-offence.html"
    },

    "vehicle-crime": {
        "name": "Vehicle Crime",
        "template": "vehicle_crime.html"
    },

    "fraud-scam": {
        "name": "Fraud / Scam",
        "template": "fraud_scam.html"
    },

    "vandalism": {
        "name": "Vandalism",
        "template": "vandalism.html"
    },

    "murder": {
        "name": "Murder",
        "template": "murder.html"
    },

    "drug-illegal-activity": {
        "name": "Drug / Illegal Activity",
        "template": "drug_illegal_activity.html"
    },

    "other-crime": {
        "name": "Other Crime",
        "template": "other_crime.html"
    }
}


# ============================================================
# REFERENCE NUMBER
# ============================================================

def create_reference():
    """
    Creates a unique Crime Spot Reporter reference number.
    Example:
    CSR-20261001-161530-123
    """

    return (
        "CSR-" +
        datetime.now().strftime(
            "%Y%m%d-%H%M%S-%f"
        )[:-3]
    )


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clean_text(value, default="Not provided"):
    """
    Cleans form input while preserving normal punctuation.
    """

    if value is None:
        return default

    value = str(value).strip()

    if not value:
        return default

    return value


def safe_category_name(category):
    """
    Creates a safe filename-friendly category name.
    """

    category = clean_text(category, "Other Crime")

    safe = secure_filename(
        category.lower()
        .replace("/", "_")
        .replace(" ", "_")
    )

    if not safe:
        safe = "other_crime"

    return safe


def allowed_evidence(filename):
    """
    Checks whether an uploaded evidence file has an allowed
    extension.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EVIDENCE_EXTENSIONS


def evidence_type(filename):
    """
    Returns image, video or unknown.
    """

    if "." not in filename:
        return "unknown"

    extension = filename.rsplit(".", 1)[1].lower()

    if extension in ALLOWED_IMAGE_EXTENSIONS:
        return "image"

    if extension in ALLOWED_VIDEO_EXTENSIONS:
        return "video"

    return "unknown"


# ============================================================
# SAVE EVIDENCE
# ============================================================

def save_evidence(category, timestamp, report_filepath):
    """
    Saves uploaded evidence safely.

    Supports:
    - Images
    - Short videos
    - Multiple files if the HTML form uses multiple uploads

    The current HTML forms can continue using:
        name="evidence"
    """

    uploaded_files = request.files.getlist("evidence")

    if not uploaded_files:
        return []

    saved_files = []

    safe_category = safe_category_name(category)

    for evidence in uploaded_files:

        if not evidence:
            continue

        if not evidence.filename:
            continue

        original_filename = secure_filename(
            evidence.filename
        )

        if not original_filename:
            continue

        if not allowed_evidence(original_filename):
            continue

        extension = original_filename.rsplit(
            ".",
            1
        )[1].lower()

        # Extra protection against unusual filenames.
        base_name = secure_filename(
            original_filename.rsplit(
                ".",
                1
            )[0]
        )

        if not base_name:
            base_name = "evidence"

        evidence_filename = (
            f"{safe_category}_"
            f"{timestamp}_"
            f"{len(saved_files) + 1}_"
            f"{base_name}.{extension}"
        )

        evidence_filepath = os.path.join(
            UPLOADS_FOLDER,
            evidence_filename
        )

        try:
            evidence.save(evidence_filepath)

            saved_files.append({
                "filename": evidence_filename,
                "type": evidence_type(evidence_filename)
            })

        except Exception:
            # Do not allow one failed upload to crash the
            # entire reporting process.
            continue

    if saved_files:

        with open(
            report_filepath,
            "a",
            encoding="utf-8"
        ) as file:

            file.write("\n")
            file.write("EVIDENCE FILES\n")
            file.write("--------------\n")

            for item in saved_files:

                file.write(
                    f"Evidence file: "
                    f"uploads/{item['filename']}\n"
                )

                file.write(
                    f"Evidence type: "
                    f"{item['type']}\n"
                )

    return saved_files


# ============================================================
# CREATE REPORT FILE
# ============================================================

def create_report(
    category,
    reference,
    date,
    time,
    location,
    description,
    extra_fields=None
):
    """
    Creates the text record for a submitted report.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    safe_category = safe_category_name(category)

    filename = (
        f"{safe_category}_"
        f"{timestamp}.txt"
    )

    filepath = os.path.join(
        SUBMISSIONS_FOLDER,
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "CRIME SPOT REPORTER\n"
        )

        file.write(
            "===================\n"
        )

        file.write(
            f"Reference Number: {reference}\n"
        )

        file.write(
            f"Crime Category: {category}\n"
        )

        file.write(
            f"Date: {date}\n"
        )

        file.write(
            f"Time: {time}\n"
        )

        file.write(
            f"Location: {location}\n"
        )

        if extra_fields:

            file.write("\n")
            file.write("ADDITIONAL INFORMATION\n")
            file.write("----------------------\n")

            for field_name, field_value in extra_fields.items():

                file.write(
                    f"{field_name}: "
                    f"{clean_text(field_value)}\n"
                )

        file.write("\n")

        file.write(
            "DESCRIPTION\n"
        )

        file.write(
            "-----------\n"
        )

        file.write(
            f"{description}\n"
        )

        file.write("\n")

        file.write(
            "Submission created: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        file.write(
            "\n"
        )

        file.write(
            "NOTE: This application is a reporting "
            "interface and does not replace emergency "
            "services or official police reporting channels.\n"
        )

    return filepath, timestamp


# ============================================================
# MAIN PAGES
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route("/report")
def report():

    return render_template(
        "report.html"
    )


# ============================================================
# CRIME CATEGORY PAGES
# ============================================================

@app.route("/theft")
def theft():

    return render_template(
        "theft.html"
    )


@app.route("/burglary")
def burglary():

    return render_template(
        "burglary.html"
    )


@app.route("/robbery")
def robbery():

    return render_template(
        "robbery.html"
    )


@app.route("/assault")
def assault():

    return render_template(
        "assault.html"
    )


@app.route("/sexual-offence")
def sexual_offence():

    return render_template(
        "sexual-offence.html"
    )


@app.route("/vehicle-crime")
def vehicle_crime():

    return render_template(
        "vehicle_crime.html"
    )


@app.route("/fraud-scam")
def fraud_scam():

    return render_template(
        "fraud_scam.html"
    )


@app.route("/vandalism")
def vandalism():

    return render_template(
        "vandalism.html"
    )


@app.route("/murder")
def murder():

    return render_template(
        "murder.html"
    )


@app.route("/drug-illegal-activity")
def drug_illegal_activity():

    return render_template(
        "drug_illegal_activity.html"
    )


@app.route("/other-crime")
def other_crime():

    return render_template(
        "other_crime.html"
    )


# ============================================================
# GENERIC SUBMISSION HANDLER
# ============================================================

def process_submission(
    category,
    extra_fields=None
):
    """
    Central submission handler used by all crime categories.
    """

    date = clean_text(
        request.form.get("date")
    )

    time = clean_text(
        request.form.get("time")
    )

    location = clean_text(
        request.form.get("location")
    )

    description = clean_text(
        request.form.get("description")
    )

    # Basic validation.
    if date == "Not provided":
        return error_page(
            "Please provide the date of the incident."
        )

    if time == "Not provided":
        return error_page(
            "Please provide the time of the incident."
        )

    if location == "Not provided":
        return error_page(
            "Please provide the location of the incident."
        )

    if description == "Not provided":
        return error_page(
            "Please provide a description of the incident."
        )

    reference = create_reference()

    report_filepath, timestamp = create_report(
        category=category,
        reference=reference,
        date=date,
        time=time,
        location=location,
        description=description,
        extra_fields=extra_fields
    )

    evidence = save_evidence(
        category,
        timestamp,
        report_filepath
    )

    return confirmation(
        category=category,
        reference=reference,
        evidence_count=len(evidence)
    )


# ============================================================
# THEFT SUBMISSION
# ============================================================

@app.route(
    "/submit-theft",
    methods=["POST"]
)
def submit_theft():

    extra_fields = {
        "Items stolen":
            request.form.get("items"),

        "Estimated value":
            request.form.get("value")
    }

    return process_submission(
        "Theft",
        extra_fields
    )


# ============================================================
# BURGLARY SUBMISSION
# ============================================================

@app.route(
    "/submit-burglary",
    methods=["POST"]
)
def submit_burglary():

    extra_fields = {
        "Property type":
            request.form.get("property"),

        "How entry was gained":
            request.form.get("entry"),

        "Stolen or damaged property":
            request.form.get("stolen"),

        "Suspect information":
            request.form.get("suspect")
    }

    return process_submission(
        "Housebreaking / Burglary",
        extra_fields
    )


# ============================================================
# ROBBERY SUBMISSION
# ============================================================

@app.route(
    "/submit-robbery",
    methods=["POST"]
)
def submit_robbery():

    extra_fields = {
        "Was a weapon used?":
            request.form.get("weapon"),

        "Items or property taken":
            request.form.get("items"),

        "Suspect description":
            request.form.get("suspect")
    }

    return process_submission(
        "Robbery",
        extra_fields
    )


# ============================================================
# ASSAULT SUBMISSION
# ============================================================

@app.route(
    "/submit-assault",
    methods=["POST"]
)
def submit_assault():

    extra_fields = {
        "Were there injuries?":
            request.form.get("injuries"),

        "Was a weapon involved?":
            request.form.get("weapon"),

        "Suspect description":
            request.form.get("suspect")
    }

    return process_submission(
        "Assault",
        extra_fields
    )


# ============================================================
# SEXUAL OFFENCE SUBMISSION
# ============================================================

@app.route(
    "/submit-sexual-offence",
    methods=["POST"]
)
def submit_sexual_offence():

    return process_submission(
        "Sexual Offence"
    )


# ============================================================
# ALL OTHER CATEGORY SUBMISSIONS
# ============================================================

@app.route(
    "/submit",
    methods=["POST"]
)
def submit():

    category = clean_text(
        request.form.get(
            "crime_category",
            "Other Crime"
        ),
        "Other Crime"
    )

    # Prevent arbitrary category strings from creating
    # confusing report names.
    known_categories = {
        config["name"]
        for config in CATEGORY_ROUTES.values()
    }

    if category not in known_categories:

        category = "Other Crime"

    return process_submission(
        category
    )


# ============================================================
# CONFIRMATION PAGE
# ============================================================

def confirmation(
    category,
    reference,
    evidence_count=0
):

    safe_category = escape(
        clean_text(category, "Crime")
    )

    safe_reference = escape(
        clean_text(reference)
    )

    if evidence_count == 1:

        evidence_message = (
            "1 evidence file was securely attached "
            "to your report."
        )

    elif evidence_count > 1:

        evidence_message = (
            f"{evidence_count} evidence files were "
            "securely attached to your report."
        )

    else:

        evidence_message = (
            "No evidence file was attached to this report."
        )

    safe_evidence_message = escape(
        evidence_message
    )

    return f"""
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            Report Submitted | Crime Spot Reporter
        </title>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{

                font-family:
                    Arial,
                    Helvetica,
                    sans-serif;

                margin: 0;

                padding: 30px 15px;

                background:
                    linear-gradient(
                        135deg,
                        #f4f7f9,
                        #e9eef2
                    );

                color: #222;

            }}

            main {{

                width: 100%;

                max-width: 650px;

                margin: 30px auto;

                background: #ffffff;

                padding: 40px 25px;

                border-radius: 16px;

                box-shadow:
                    0 8px 30px
                    rgba(0, 0, 0, 0.12);

                text-align: center;

            }}

            .success-icon {{

                width: 70px;

                height: 70px;

                margin: 0 auto 20px;

                border-radius: 50%;

                display: flex;

                align-items: center;

                justify-content: center;

                background: #e8f5e9;

                font-size: 38px;

            }}

            h1 {{

                margin: 0 0 15px;

                font-size: 28px;

            }}

            .category {{

                font-weight: bold;

            }}

            .reference-label {{

                margin-top: 30px;

                margin-bottom: 8px;

                font-weight: bold;

            }}

            .reference {{

                font-size: 25px;

                font-weight: bold;

                letter-spacing: 1px;

                padding: 18px;

                border: 2px solid #222;

                border-radius: 10px;

                background: #f8f9fa;

                word-break: break-word;

                user-select: all;

            }}

            .evidence {{

                margin: 20px 0;

                padding: 15px;

                border-radius: 8px;

                background: #f4f6f8;

                font-size: 14px;

            }}

            .buttons {{

                margin-top: 25px;

                display: flex;

                flex-wrap: wrap;

                justify-content: center;

                gap: 10px;

            }}

            button {{

                border: none;

                border-radius: 8px;

                padding: 13px 18px;

                cursor: pointer;

                font-size: 15px;

                font-weight: bold;

            }}

            .primary {{

                background: #222;

                color: white;

            }}

            .secondary {{

                background: #e9ecef;

                color: #222;

            }}

            .share {{

                background: #198754;

                color: white;

            }}

            button:hover {{

                opacity: 0.9;

            }}

            .notice {{

                margin-top: 30px;

                padding-top: 20px;

                border-top: 1px solid #ddd;

                font-size: 13px;

                color: #666;

                line-height: 1.5;

            }}

            @media (max-width: 500px) {{

                main {{

                    padding: 30px 18px;

                    margin: 15px auto;

                }}

                h1 {{

                    font-size: 24px;

                }}

                .reference {{

                    font-size: 20px;

                }}

                .buttons {{

                    flex-direction: column;

                }}

                button {{

                    width: 100%;

                }}

            }}

        </style>

    </head>

    <body>

        <main>

            <div class="success-icon">
                ✓
            </div>

            <h1>
                Report Submitted
            </h1>

            <p>
                Your
                <span class="category">
                    {safe_category}
                </span>
                report has been recorded successfully.
            </p>

            <p class="reference-label">
                Your report reference number:
            </p>

            <div
                class="reference"
                id="reference"
            >
                {safe_reference}
            </div>

            <div class="evidence">
                {safe_evidence_message}
            </div>

            <p>
                Please keep your reference number
                for your records.
            </p>

            <div class="buttons">

                <button
                    class="share"
                    onclick="shareReference()"
                >
                    Share Reference
                </button>

                <button
                    class="primary"
                    onclick="window.location.href='/report'"
                >
                    Report Another Crime
                </button>

                <button
                    class="secondary"
                    onclick="window.location.href='/'"
                >
                    Return Home
                </button>

            </div>

            <div class="notice">

                <strong>Important:</strong>

                Crime Spot Reporter is a community
                reporting application and does not
                replace emergency services or official
                police reporting channels.

                If you are in immediate danger,
                contact the appropriate emergency
                services.

            </div>

        </main>

        <script>

            function shareReference() {{

                const reference =
                    {safe_reference!r};

                const category =
                    {safe_category!r};

                const message =
                    "Crime Spot Reporter\\n" +
                    "Report category: " +
                    category +
                    "\\n" +
                    "Reference number: " +
                    reference;

                if (
                    navigator.share
                ) {{

                    navigator.share({{

                        title:
                            "Crime Spot Reporter",

                        text:
                            message

                    }}).catch(
                        function(error) {{

                            console.log(
                                "Sharing cancelled:",
                                error
                            );

                        }}
                    );

                }} else if (
                    navigator.clipboard
                ) {{

                    navigator.clipboard
                        .writeText(message)
                        .then(function() {{

                            alert(
                                "Reference details copied "
                                + "to your clipboard."
                            );

                        }})
                        .catch(function() {{

                            alert(
                                "Your reference number is: "
                                + reference
                            );

                        }});

                }} else {{

                    alert(
                        "Your reference number is: "
                        + reference
                    );

                }}

            }}

        </script>

    </body>

    </html>
    """


# ============================================================
# ERROR PAGE
# ============================================================

def error_page(message):

    safe_message = escape(
        clean_text(message)
    )

    return f"""
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            Submission Error | Crime Spot Reporter
        </title>

        <style>

            body {{

                font-family:
                    Arial,
                    Helvetica,
                    sans-serif;

                background: #f5f5f5;

                margin: 0;

                padding: 30px 15px;

            }}

            main {{

                max-width: 600px;

                margin: 50px auto;

                padding: 35px 25px;

                background: white;

                border-radius: 12px;

                text-align: center;

                box-shadow:
                    0 5px 20px
                    rgba(0,0,0,0.1);

            }}

            .error {{

                padding: 15px;

                margin: 20px 0;

                border-radius: 8px;

                background: #fff3cd;

                color: #664d03;

            }}

            button {{

                padding: 12px 20px;

                border: none;

                border-radius: 7px;

                background: #222;

                color: white;

                cursor: pointer;

                font-size: 15px;

            }}

        </style>

    </head>

    <body>

        <main>

            <h1>
                Submission Could Not Be Completed
            </h1>

            <div class="error">
                {safe_message}
            </div>

            <button
                onclick="history.back()"
            >
                Go Back
            </button>

        </main>

    </body>

    </html>
    """


# ============================================================
# UPLOAD SIZE ERROR
# ============================================================

@app.errorhandler(413)
def request_too_large(error):

    return error_page(
        "The submission is too large. "
        "Please reduce the size of your evidence "
        "files and try again."
    ), 413


# ============================================================
# GENERAL ERROR HANDLER
# ============================================================

@app.errorhandler(500)
def internal_error(error):

    return error_page(
        "Something went wrong while processing "
        "the report. Please try again."
    ), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "application": "Crime Spot Reporter"
    }


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    # Debug is intentionally disabled for normal running.
    # For local development you can temporarily change
    # debug=False to debug=True if necessary.

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )

