package distmedia

import (
	"context"
	"github.com/pantyukhov/distmedia/projects/pubsub/services/distmedia/infrastructure/config"
	"github.com/pantyukhov/distmedia/projects/pubsub/services/distmedia/infrastructure/service"
	"github.com/pantyukhov/distmedia/projects/pubsub/services/distmedia/routes"
	"go.uber.org/fx"
)

func initApp(f func(engine *Engine)) *fx.App {
	app := fx.New(
		fx.Provide(context.Background),
		service.Module,
		config.Module,

		//routes
		fx.Provide(routes.NewPublisherRoute),

		fx.Provide(NewEngine),
		fx.Invoke(f),
	)

	return app
}

func Start(ctx context.Context) error {
	var globalError error
	app := initApp(func(engine *Engine) {
		globalError = engine.Start(ctx)
		return
	})

	if err := app.Start(ctx); err != nil {
		globalError = err
	}

	return globalError
}
