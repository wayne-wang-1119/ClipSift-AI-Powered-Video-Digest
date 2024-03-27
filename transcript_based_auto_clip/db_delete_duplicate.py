import weaviate
from collections import defaultdict


def fetch_all_transcript_segments(client):
    """
    Fetch all transcript segments from Weaviate.
    """
    query = "{ Get { TranscriptSegment { text start duration videoId } } }"
    result = client.query.raw(query)

    if "errors" in result:
        raise Exception(f"Error fetching segments: {result['errors']}")

    return result.get("data", {}).get("Get", {}).get("TranscriptSegment", [])


def find_duplicates(segments):
    """
    Identify duplicate segments based on text, start, videoId, and duration.
    Returns a list of UUIDs for the duplicates (excluding the first occurrence).
    """
    seen = set()
    duplicates = []
    for segment in segments:
        identifier = (segment["videoId"],)
        if identifier in seen:
            duplicates.append(segment["videoId"])
        else:
            seen.add(identifier)
    return duplicates


def delete_segments_by_uuid(client, uuids):
    """
    Delete segments identified by their UUIDs.
    """
    client.batch.delete_objects(
        class_name="TranscriptSegment",
        where={"path": ["videoId"], "operator": "ContainsAny", "valueTextArray": uuids},
    )


def main():
    client = weaviate.Client("http://localhost:8080")

    segments = fetch_all_transcript_segments(client)
    print(f"Fetched {len(segments)} segments.")

    duplicate_uuids = find_duplicates(segments)
    print(f"Identified {len(duplicate_uuids)} duplicates to delete.")

    delete_segments_by_uuid(client, duplicate_uuids)
    print("Duplicate deletion process completed.")


if __name__ == "__main__":
    main()
