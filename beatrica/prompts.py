prompts = {
    "get_changes": {
        "question": "What are the changes in the following code? Write one change per unique commit hash please. ",
        "expected_answer": "Write the answer in the following format: <xml><changes><change commit='commit_hash1'>change 1 for commit_hash1, change 2 for commit_hash1</change><change commit='commit_hash2'>change 1 for commit_hash2</change>...</changes></xml>",
        "expected_pattern": r"<change commit='(.*?)'>(.*?)<\/change>",
    },
    "can_review": {
        "question": "Can you review and suggest points for improvement of the change in the following code? Answer only with number 1 if you can review the code or 0 if you cannot. The change is: ",
        "expected_answer": "Write the answer in the following format: <xml><review>1</review></xml>",
        "expected_pattern": r"<review>(.*?)<\/review>",
    },
    "make_review": {
        "question": "You are code reviewer. Please review the following code change and suggest points for improvement. The change is: ",
        "expected_answer": "Write the answer in the following format: <xml><review><point>point 1</point><point>point 2</point>...</review></xml>",
        "expected_pattern": r"<point>(.*?)<\/point>",
    },
    "aggregate_review_points": {
        "question": "Please aggregate the concrete review points for the concrete code change. The review points are: ",
        "expected_answer": "Write the answer in the following format: <xml><aggregated_review>Aggregated review text as a suggestion</aggregated_review></xml>",
        "expected_pattern": r"<aggregated_review>(.*?)<\/aggregated_review>",
    },
}