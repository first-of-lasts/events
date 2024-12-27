from dishka import Provider, provide, Scope, AnyOf

from events.application.interfaces import location_interface
from events.application.interactors import location_interactor
from events.infrastructure.gateways.location_gateway import LocationGateway


class LocationProvider(Provider):
    location_gateway = provide(
        source=LocationGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            location_interface.CountryReader, location_interface.RegionReader,
        ]
    )

    @provide(scope=Scope.REQUEST)
    def get_countries_interactor(
            self,
            location_gateway: location_interface.CountryReader,
    ) -> location_interactor.GetCountriesInteractor:
        return location_interactor.GetCountriesInteractor(
            location_gateway=location_gateway
        )

    @provide(scope=Scope.REQUEST)
    def get_regions_interactor(
            self,
            location_gateway: location_interface.RegionReader,
    ) -> location_interactor.GetRegionsInteractor:
        return location_interactor.GetRegionsInteractor(
            location_gateway=location_gateway
        )
