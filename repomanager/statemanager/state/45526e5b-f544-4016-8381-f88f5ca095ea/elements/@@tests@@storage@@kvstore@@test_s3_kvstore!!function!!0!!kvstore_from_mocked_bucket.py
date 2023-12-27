def kvstore_from_mocked_bucket() -> Generator[S3DBKVStore, None, None]:
    with mock_s3():
        s3 = boto3.resource("s3")
        bucket = s3.Bucket("test_bucket")
        bucket.create(CreateBucketConfiguration={"LocationConstraint": "us-west-1"})
        yield S3DBKVStore(bucket)
