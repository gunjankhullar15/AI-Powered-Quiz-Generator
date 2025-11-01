from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.database import AsyncSessionLocal
from app.models.weightage import Weightage

async def seed_fixed_weightages():
    """Seed fixed global weightage values when app starts"""
    print(" Setting fixed global weightage values...")
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if weightages already exist
            result = await session.execute(select(Weightage))
            existing_weightages = result.scalars().all()
            
            if existing_weightages:
                print(" Fixed weightages already exist in database.")
                return
            
            # Fixed global weightage values (same for all tests)
            fixed_weightages = [
                {'question_type': 'MCQ', 'weightage': 1},
                {'question_type': 'Scenario_Based', 'weightage': 3},
                {'question_type': 'Fill_Blanks', 'weightage': 1},
                {'question_type': 'True_False', 'weightage': 1}
            ]
            
            # Add fixed weightages to database
            for weightage_data in fixed_weightages:
                weightage = Weightage(**weightage_data)
                session.add(weightage)
                print(f" Set {weightage_data['question_type']}: {weightage_data['weightage']} points")
            
            await session.commit()
            print(" Fixed global weightage values set successfully!")
            
        except Exception as e:
            await session.rollback()
            print(f" Error setting weightages: {e}")