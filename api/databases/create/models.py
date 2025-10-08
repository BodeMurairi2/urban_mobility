#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class PaymentTypes(Base):
    __tablename__ = "payment_types"
    payment_type_id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)

    # Relationship with Trips
    trips = relationship("Trips", back_populates="payment_type")


class RateCodes(Base):
    __tablename__ = "rate_codes"
    rate_code_id = Column(Integer, primary_key=True)
    description = Column(String(50), nullable=False)

    trips = relationship("Trips", back_populates="rate_code")


class Vendors(Base):
    __tablename__ = "vendors"
    vendor_id = Column(Integer, primary_key=True)
    vendor_name = Column(String(50), nullable=False)

    trips = relationship("Trips", back_populates="vendor")


class TaxiZones(Base):
    __tablename__ = "taxi_zones"
    location_id = Column(Integer, primary_key=True)
    borough = Column(String(50), nullable=False)
    zone = Column(String(50), nullable=False)
    service_zone = Column(String(50), nullable=False)

    # Trips where this zone is the pickup location
    trips_pu = relationship(
        "Trips",
        foreign_keys="[Trips.pu_location_id]",
        back_populates="pickup_location",
        overlaps="pickup_location"
    )

    # Trips where this zone is the dropoff location
    trips_do = relationship(
        "Trips",
        foreign_keys="[Trips.do_location_id]",
        back_populates="dropoff_location",
        overlaps="dropoff_location"
    )


class Trips(Base):
    __tablename__ = "trips"
    trip_id = Column(Integer, primary_key=True)
    pickup_datetime = Column(DateTime, nullable=False)
    dropoff_datetime = Column(DateTime, nullable=False)
    passenger_count = Column(Integer, nullable=False)
    trip_distance = Column(Float, nullable=False)
    store_and_fwd_flag = Column(String(1), nullable=False)
    fare_amount = Column(Float, nullable=False)
    extra = Column(Float, nullable=False)
    mta_tax = Column(Float, nullable=False)
    tip_amount = Column(Float, nullable=False)
    tolls_amount = Column(Float, nullable=False)
    improvement_surcharge = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)

    # Foreign keys
    payment_type_id = Column(Integer, ForeignKey("payment_types.payment_type_id"))
    rate_code_id = Column(Integer, ForeignKey("rate_codes.rate_code_id"))
    pu_location_id = Column(Integer, ForeignKey("taxi_zones.location_id"))
    do_location_id = Column(Integer, ForeignKey("taxi_zones.location_id"))
    vendor_id = Column(Integer, ForeignKey("vendors.vendor_id"))

    # Relationships
    payment_type = relationship("PaymentTypes", back_populates="trips")
    rate_code = relationship("RateCodes", back_populates="trips")
    vendor = relationship("Vendors", back_populates="trips")

    pickup_location = relationship(
        "TaxiZones",
        foreign_keys=[pu_location_id],
        back_populates="trips_pu",
        overlaps="trips_pu"
    )
    dropoff_location = relationship(
        "TaxiZones",
        foreign_keys=[do_location_id],
        back_populates="trips_do",
        overlaps="trips_do"
    )
