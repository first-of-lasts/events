from dishka import Provider, provide, Scope, AnyOf

from events.application.interfaces import location_interface
from events.application.interactors import location_interactor
from events.application.services.location_validator import LocationValidator
from events.infrastructure.gateways.location_gateway import LocationGateway


class LocationProvider(Provider):
    location_gateway = provide(
        source=LocationGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            location_interface.LocationGatewayInterface,
            location_interface.CountryReader,
            location_interface.RegionReader,
        ]
    )

    @provide(scope=Scope.REQUEST)
    def list_countries_interactor(
            self,
            location_gateway: location_interface.CountryReader,
    ) -> location_interactor.ListCountriesInteractor:
        return location_interactor.ListCountriesInteractor(
            location_gateway=location_gateway
        )

    @provide(scope=Scope.REQUEST)
    def list_regions_interactor(
            self,
            location_gateway: location_interface.RegionReader,
    ) -> location_interactor.ListRegionsInteractor:
        return location_interactor.ListRegionsInteractor(
            location_gateway=location_gateway
        )

    @provide(scope=Scope.REQUEST)
    def get_location_validator(
            self,
            location_gateway: location_interface.LocationGatewayInterface
    ) -> LocationValidator:
        return LocationValidator(location_gateway=location_gateway)
