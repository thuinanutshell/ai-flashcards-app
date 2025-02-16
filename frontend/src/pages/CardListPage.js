import React from 'react';
import { useParams } from 'react-router-dom';
import CardList from '../cards/CardList';

const CardListPage = () => {
    const { folderId } = useParams();

    return (
        <div className="container mx-auto px-4 py-8">
            <CardList folderId={folderId} />
        </div>
    );
};

export default CardListPage;
