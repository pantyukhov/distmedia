package storage

import "context"

type UploadReq struct {
}

type Service interface {
	Upload(ctx context.Context, req *UploadReq) error
}
