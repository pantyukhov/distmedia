package storage

import (
	"context"
	"errors"
	"github.com/pantyukhov/distmedia/projects/pubsub/pkg/domain/service/storage"
)

type Service struct {
}

func (s *Service) Upload(ctx context.Context, req *storage.UploadReq) error {
	return errors.New("unsupportd")
}
